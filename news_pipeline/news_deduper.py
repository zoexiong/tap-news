# -*- coding: utf-8 -*-

import datetime
import os
import sys

from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloudAMQP_client import CloudAMQPClient

# Use your own Cloud AMQP queue
DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://lqjaykhn:5-55AsYfCgoc0jXcrILXCdrPhmpUWOmJ@donkey.rmq.cloudamqp.com/lqjaykhn"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"

# it's local operation, no need to worry about get blocked
SLEEP_TIME_IN_SECONDS = 1

NEWS_TABLE_NAME = "news"

# todo: need to do research to calculate a more accurate number
SAME_NEWS_SIMILARITY_THRESHOLD = 0.8

cloudAMQP_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not isinstance(msg, dict) :
        return

    task = msg
    text = str(task['text'])
    if text is None:
        return

    # get all recent news based on publishedAt
    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day - 1, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=2)

    db = mongodb_client.get_db()
    # gte: greater or equal; lt: less than
    recent_news_list = list(db[NEWS_TABLE_NAME].find({'publishedAt': {'$gte': published_at_day_begin, '$lt': published_at_day_end}}))
    print 'number of recent news: %s' % len(recent_news_list)

    if recent_news_list is not None and len(recent_news_list) > 0:
        documents = [str(news['text']) for news in recent_news_list]
        documents.insert(0, text)

        # Calculate similarity matrix
        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T

        # output as array
        print pairwise_sim.A

        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                # Duplicated news. Ignore.
                print "Duplicated news. Ignore."
                return

    # turn the datetime string into date format supported by mongodb to enable search by publishedAt attribute
    task['publishedAt'] = parser.parse(task['publishedAt'])

    # if exists, overwrite it, if not, insert
    db[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)
    print "one news added to database"

while True:
    if cloudAMQP_client is not None:
        msg = cloudAMQP_client.getMessage()
        if msg is not None:
            # Parse and process the task
            try:
                handle_message(msg)
            except Exception as e:
                print e
                pass

        cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
