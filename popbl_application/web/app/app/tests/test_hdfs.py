from django.test import TestCase
from app.hdfs import insert_hdfs_tweet
import requests


class HDFSRequestTest(TestCase):
    def test_file_insert(self):
        text = "awesome twit"
        filename = insert_hdfs_tweet(text, "unit-test")
        r1 = requests.get(
            "http://node1.itapp.eus:9870/webhdfs/v1/unit-test/"
            + filename
            + ".json?user.name=hadoop&op=OPEN&noredirect=true"
        )
        data = r1.json()
        url = data["Location"]
        url = url[7:]
        idx = url.index(":")
        url = "http://" + url[:idx] + ".itapp.eus" + url[idx:]
        response = requests.get(url)
        assert response.status_code == 200
        decoded = response.content.decode("utf-8")
        assert text in decoded
