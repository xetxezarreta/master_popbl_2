from django.forms import Form, CharField, Textarea, TextInput


class TopicForm(Form):
    introduced_topic = CharField(widget=TextInput(attrs={"type": "text"}))


class TweetForm(Form):
    generated_tweet = CharField(widget=Textarea(attrs={"rows": 10, "cols": 100}))
