import json

# Web App
# Parse:
# Content from article
# Author
# Date
# Title
# Return a json with url details when accessed with GET /URL/{id}


def connect_to_url(url):
    web_resp = {
        'Content': 'Lies on lies.',
        'Author': 'Scrub McDuckerson',
        'Date': '2020/2/20',
        'Title': 'Always lying',
        'URL': url
    }
    return json.dumps({'resp': web_resp}, indent=4)

def parse_data():
    return

def run():
    print('\nHello Humanoid.\nYour choices are:')
    print('    1. Detect fake news.')
    print('    2. Go away.')
    ans = int(input('What say you? '))
    if ans == 1:
        url = input('In order to determine whether you are being lied to, enter a URL: ')
        response = connect_to_url(url)
        print(response)

    print('Womp womp.')
