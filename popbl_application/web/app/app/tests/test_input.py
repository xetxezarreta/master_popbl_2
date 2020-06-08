from django.test import TestCase
from app.input import Input
import os
import json


class InputTest(TestCase):
    def test_allowed_input_validator(self):
        inp = Input()
        with open("app/tests/allowed.json", encoding="utf-8") as json_file:
            data = json.load(json_file)
            for elem in data:
                san = inp.sanizate(elem)
                res_topic = inp.validate_topic(san)
                res_tweet = inp.validate_tweet(san)
                assert res_topic == True
                assert res_tweet == True

    def test_not_allowed_input_validator(self):
        inp = Input()
        with open("app/tests/not_allowed.json", encoding="utf-8") as json_file:
            data = json.load(json_file)
            for elem in data:
                san = inp.sanizate(elem)
                res_topic = inp.validate_topic(san)
                assert res_topic == False
