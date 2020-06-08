from django.test import TestCase
import elasticsearch_dsl
from app.models.elastic_model import insert_tweet, query_timestamp_range, TweetModel
import mock


class hit:
    def __init__(self, tweet, date):
        self.tweet = tweet
        self.date = date


def mock_execute():
    list_res = []
    list_res.append(hit("Text-test1", "date1"))
    list_res.append(hit("Text-test2", "date2"))
    return list_res


@mock.patch("elasticsearch_dsl.Search.execute", side_effect=mock_execute)
class ESQueryTestMock(TestCase):
    def test_query(self, mock_execute):

        search = query_timestamp_range("2020-05-20", "2020-05-29")
        print("mock res", search)
        count = 0
        for hit in search:
            print(hit.tweet)
            if count == 0:
                assert hit.tweet == "Text-test1"
                assert hit.date == "date1"
            else:
                assert hit.tweet == "Text-test2"
                assert hit.date == "date2"
            count = count + 1
        assert count == 2

    def test_tweet_model(self, mock_execute):
        tm = TweetModel("text", "date")
        assert tm.tweet == "text"
        assert tm.date == "date"
