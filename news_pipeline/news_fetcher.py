# -*- coding: utf-8 -*-

import os
import sys

# from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import news_scraper
from cloudAMQP_client import CloudAMQPClient

# Use your own Cloud AMQP queue
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://lqjaykhn:5-55AsYfCgoc0jXcrILXCdrPhmpUWOmJ@donkey.rmq.cloudamqp.com/lqjaykhn"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"
SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://hoamejlv:tlr-stbY0WU6WCR9rgEfEdzFuANiRj0K@donkey.rmq.cloudamqp.com/hoamejlv"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print 'message is broken'
        return

    task = msg

    # now we only support CNN

    if task['source'] == 'cnn' or task['source'] == 'bbc-news':
        print 'Scraping news from [%s]' % task['source']
        text = news_scraper.extract_news(task['url'],task['source'])
        task['text'] = text
        dedupe_news_queue_client.sendMessage(task)
    else:
        print 'News source [%s] is not supported.' % task['source']

    # article = Article(task['url'])
    # article.download()
    # article.parse()
    #
    # print article.text
    #
    # task['text'] = article.text

while True:
    # fetch msg from queue
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            # Handle message
            try:
                handle_message(msg)
            except Exception as e:
                print e
                # continue
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)

# todo: refactor AMQPclient and use a separate method to send ack only when the received message was processed successfully