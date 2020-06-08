import socket

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .forms import TopicForm, TweetForm
from .models.elastic_model import insert_tweet, query_timestamp_range, TweetModel
from .hdfs import insert_hdfs_tweet
from .tensorflow.predict import predict_tweet
from .input import Input

topic = ""
tweet = ""
tweet_list = []


def introduced_topic(request):
    global topic, tweet
    inp = Input()
    alert_message = ""
    error = False
    topic = request.POST["introduced_topic"]
    # sanitization + validation
    topic = inp.sanizate(topic)
    print("TOPIC: " + topic)
    is_valid = inp.validate_topic(topic)
    # generate tweet
    if is_valid:
        tweet = predict_tweet(topic)
    else:
        error = True
        alert_message = "Introduced topic is not valid! Allowed: [a-zA-Z0-9] and [.,;] and single quote"
    return error, alert_message


def publish_generated_tweet(request):
    global tweet
    inp = Input()
    alert_message = ""
    error = False
    tweet = request.POST["generated_tweet"]
    # sanitization + validation
    generated_tweet = inp.sanizate(tweet)
    is_valid = inp.validate_tweet(generated_tweet)
    if is_valid:
        # post tweet on twitter
        print(generated_tweet)
        # save tweet on elastic
        insert_tweet(generated_tweet)
        # save tweet on hdfs
        insert_hdfs_tweet(generated_tweet, "twitter")
    else:
        error = True
        alert_message = "Introduced tweet is not valid! Allowed: [a-zA-Z0-9] and [.,;] and single quote"
    return error, alert_message


def get_tweet_list(request):
    global tweet_list
    filtered_tweets = query_timestamp_range(request.POST["from"], request.POST["to"])
    tweet_list = []
    for hit in filtered_tweets:
        print(hit.tweet)
        tw = TweetModel(hit.tweet, str(hit.date).split("T")[0])
        tweet_list.append(tw)


@csrf_exempt
def home_view(request):
    global topic, tweet, tweet_list
    alert_message = ""
    error = False
    if request.method == "POST":
        if "introduced_topic" in request.POST:
            error, alert_message = introduced_topic(request)
        elif "generated_tweet" in request.POST:
            error, alert_message = publish_generated_tweet(request)
        elif "from" in request.POST:
            get_tweet_list(request)
        topic_form = TopicForm(initial={"introduced_topic": topic})
        tweet_form = TweetForm(initial={"generated_tweet": tweet})
    elif request.method == "GET":
        topic = ""
        tweet = ""
        tweet_list = []
        topic_form = TopicForm()
        tweet_form = TweetForm()
    else:
        return redirect("/")

    return render(
        request,
        "index.html",
        {
            "tweet_list": tweet_list,
            "topic_form": topic_form,
            "tweet_form": tweet_form,
            "hostname": socket.gethostname(),
            "error": error,
            "alert_message": alert_message,
        },
    )
