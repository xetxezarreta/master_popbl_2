import time
import requests
import datetime
import time
import json


def insert_hdfs_tweet(tweet, folder):
    ts = time.time()

    milliseconds = int(round(time.time() * 1000))
    tweet = {
        "Text": tweet,
        "Source": "Itapp",
        "TimeStamp": datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S"),
    }

    r1 = requests.put(
        "http://node1.itapp.eus:9870/webhdfs/v1/"
        + folder
        + "/generated-twit-"
        + str(milliseconds)
        + ".json?user.name=hadoop&op=CREATE&noredirect=true"
    )
    data = r1.json()
    url = data["Location"]
    url = url[7:]
    idx = url.index(":")
    url = "http://" + url[:idx] + ".itapp.eus" + url[idx:]
    requests.put(url, data=json.dumps(tweet))
    return "generated-twit-" + str(milliseconds)
