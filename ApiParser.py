import requests
import pandas as pd


def sendPost(response_num):
    dictToSend = get_api_response(response_num)
    print(f'\n{dictToSend}\n')
    res = requests.post('http://localhost:5000/api/v1/KB', json=dictToSend)
    print(f'\nSERVER RESPONSE: {res.text}')
    dictFromServer = res.json()
    print(f'\nJSON PACKAGE RETURNED: {dictFromServer}\n')


def get_api_response(case):
    resp = {
        1: {
               "url": "https://www.nytimes.com/news_article/",
               "post_data": {
                     "account_name": "@test_account",
                     "user_name": "Sally Smith",
                     "post_body": "WOW! Look at this article!",
                     "post_date_time": "2020-10-06T011:24PST",
                     "account_age": "4.3",
                     "profile_picture": "True"
                },
               "page_data": {
                     "title": "End of the World Scheduled for Next Week",
                     "subtitle": "Participants of the year 2020 are unsurprised",
                     "authors": "[Robert Joe, Joseph Bob]",
                     "publisher": "NYT",
                     "publish_date": "null",
                     "publish_date_time": "2020-10-05T09:53PST",
                     "body": "As a horrible year comes to a close, nobody is surprised by the anouncement...",
                     "citation_urls": "[http://www.wikipedia.org/, http://www.un.org/]",
                     "html": '<!doctype html><html lang="en"><head>...'
               }
            },
        2: {
                "url": "www.cnn.com/news_article/",
                "post_data": {
                     "account_name": "",
                     "user_name": "",
                     "post_body": "",
                     "post_date_time": "",
                     "account_age": "",
                     "profile_picture": ""
                },
                "page_data": {
                     "title": "",
                     "subtitle": "",
                     "authors": "",
                     "publisher": "",
                     "publish_date": "",
                     "publish_date_time": "",
                     "body": "",
                     "citation_urls": "",
                     "html": ''
                }
            },
        3: {
            "url": "http://www.cnn.com/",
            "post_data": {
                "account_name": "",
                "user_name": "",
                "post_body": "!",
                "post_date_time": "",
                "account_age": "",
                "profile_picture": ""
            },
            "page_data": {
                "title": "Lies on lies with fake news.",
                "subtitle": "",
                "authors": "",
                "publisher": "",
                "publish_date": "",
                "publish_date_time": "",
                "body": "",
                "citation_urls": "",
                "html": ''
            }
        },
    }

    return resp[case]


def parse_api(jsonPackage):
    try:
        title = jsonPackage['page_data']['title'] if len(jsonPackage['page_data']['title']) > 0 else ""
        text = jsonPackage['page_data']['body'] if len(jsonPackage['page_data']['body']) > 0 else ""
        date = jsonPackage['page_data']['publish_date'] if len(jsonPackage['page_data']['publish_date']) > 0 else ""
        bodyDF = {
            'title': [title],
            'text': [text],
            'subject': ['News'],
            'date': [date]
        }
        bodyDF = pd.DataFrame.from_dict(bodyDF)

        parsedUrl = Parser(jsonPackage['url']).get_url()
        urlDF = pd.DataFrame()
        urlDF['domain_type'] = [parsedUrl['domain_type']]
        urlDF['protocol'] = [parsedUrl['protocol']]
    except:
        bodyDF = None
        urlDF = None

    return bodyDF, urlDF











class Parser:
    def __init__(self, url):
        try:
            if url[:4] != "http":
                self.url = requests.head("http://" + url).headers['location']
            else:
                self.url = requests.head(url).headers['location']
        except Exception:
            self.url = url

        self.data = {}

    def get_url(self):
        self.protocolEncoder()
        self.domainEncoder()

        return self.data

    def protocolEncoder(self):
        link = self.url
        if isinstance(link, float):
            self.data['protocol'] = 0
        elif link[:5] == "https":
            self.data['protocol'] = 2
        elif link[:4] == "http":
            self.data['protocol'] = 1
        else:
            self.data['protocol'] = 0

    def domainEncoder(self):
        domain = [".com/", ".org/", ".edu/", ".gov/", ".uk/", ".net/", ".ca/", ".de/", ".jp/", ".fr/", ".au/", ".us/",
                  ".ru/", ".ch/", ".it/", ".nl/", ".se/", ".no/", ".es/", ".mil/", ".ly/", ".tel/", ".kitchen/",
                  ".email/", ".tech/", ".estate/", ".xyz/", ".codes/", ".bargains/", ".bid/", ".expert/", ".co/",
                  ".name/", ".mobi/", ".asia/", ".biz/", ".arpa/", ".cat/", ".jobs/", ".info/", ".int/", ".pro/",
                  ".aero/", ".travel/", ".coop/"]

        default = len(domain)
        if isinstance(self.url, float):
            self.data['domain_type'] = default
        i = 0
        while i < len(domain) and domain[i] not in self.url:
            i += 1

        self.data['domain_type'] = i if i < len(domain) else len(domain)
