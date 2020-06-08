from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections, Document, Date, Text, Search


class TweetModel:

    tweet = None
    date = None

    def __init__(self, txt, date):
        self.tweet = txt
        self.date = date

    def tweet(self):
        return tweet

    def date(self):
        return date


class Tweet(Document):
    tweet = Text()
    date = Date()

    class Index:
        name = "itapp"
        settings = {
            "number_of_shards": 2,
        }

    def save(self, **kwargs):
        return super(Tweet, self).save(**kwargs)

    def is_published(self):
        return datetime.now() > self.published_from


def insert_tweet(tweet_content):
    try:
        # create conection
        connections.create_connection(hosts=["node1.itapp.eus:9200"])
        # create the mappings in elasticsearch
        Tweet.init()
        # create and save the tweet
        tweet = Tweet(tweet=tweet_content, date=datetime.now())
        tweet.save()
    except Exception:
        pass


def query_timestamp_range(ts1, ts2):
    try:
        client = Elasticsearch(hosts="node1.itapp.eus:9200")
        s = (
            Search(using=client, index="itapp")
            .filter("range", **{"date": {"gte": ts1, "lt": ts2,}})
            .extra(size=10)
        )
        response = s.execute()
        print(response)
        print(s)
    except Exception:
        response = ""
        print(response)
    return s
