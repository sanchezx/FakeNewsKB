import requests
import pandas as pd

def get_api_response():
    resp = {
       "url": "https://www.example.com/news_article/",
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
    }

    return resp


def parse_api(jsonPackage):
    bodyDF = {
        'title': jsonPackage['page_data']['title'],
        'text': jsonPackage['page_data']['body'],
        'subject': 'News',
        'date': jsonPackage['page_data']['publish_date']
    }
    bodyDF = pd.DataFrame.from_dict(bodyDF)

    encodeUrl = UrlParser(jsonPackage['url']).execute()
    urlDF = pd.DataFrame()
    urlDF['domain_type'] = [encodeUrl['domain_type']]
    urlDF['protocol'] = [encodeUrl['protocol']]

    return bodyDF, urlDF


def sendPost():
    dictToSend = get_api_response()
    print(dictToSend)
    res = requests.post('http://localhost:5000/api/v1/webApp', json=dictToSend)
    print('response from server:', res.text)
    dictFromServer = res.json()
    print(dictFromServer)


class UrlParser:
    def __init__(self, url):
        try:
            if url[:4] != "http":
                self.url = requests.head("http://" + url).headers['location']
            else:
                self.url = requests.head(url).headers['location']
        except Exception:
            self.url = url

        self.data = {}

    def execute(self):
        self.protocolEncoder()
        self.domainEncoder()

        return self.data

    def protocolEncoder(self):
        # Protocols for encryption grade
        # protocol = ["no_protocol", "http", "https"]
        # protocol_encoding = [0, 1, 2]
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
        while domain[i] not in self.url and i < len(domain):
            i += 1
        self.data['domain_type'] = i
