from django.test import TestCase
from app.forms import TopicForm, TweetForm


class TopicFormTest(TestCase):
    def test_form(self):
        form_data = {"introduced_topic": "Ander"}
        form = TopicForm(data=form_data)
        self.assertTrue(form.is_valid())


class TweetFormTest(TestCase):
    def test_form(self):
        form_data = {"generated_tweet": "Hola me llamo Ander"}
        form = TweetForm(data=form_data)
        self.assertTrue(form.is_valid())
