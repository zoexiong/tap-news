import os
import random
import requests

from lxml import html

GET_CNN_NEWS_XPATH = '''//p[@class="zn-body__paragraph speakable"]//text() | //div[@class='zn-body__paragraph speakable']//text() | //p[@class="zn-body__paragraph"]//text() | //div[@class="zn-body__paragraph"]//text()'''

# Load user agents in case got blocked
USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []

with open(USER_AGENTS_FILE, 'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])
random.shuffle(USER_AGENTS)

def getHeaders():
    ua = random.choice(USER_AGENTS)
    headers = {
        "Connection" : "close",
        # if don't indicate user-agent here, will be marked as python request
        "User-Agent" : ua
    }
    return headers

def extract_news(news_url):
    # Fetch html
    # use session instead of simply use get to pretent this is not send by a robot
    session_requests = requests.session()
    response = session_requests.get(news_url, headers=getHeaders())

    news = {}

    try:
        # Parse html
        tree = html.fromstring(response.content)
        # Extract information
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        # join news list
        news = ''.join(news)
    except Exception as e:
        print e
        return {}

    return news
