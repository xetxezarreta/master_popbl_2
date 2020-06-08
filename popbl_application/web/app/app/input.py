import string
import re


class Input:
    def __init__(self):
        return

    def validate_topic(self, text):
        val = re.compile(r"^[a-zA-Z\s\n,'.;]{3,50}$")
        try:
            result = val.search(text)
            if result is None:
                return False
            else:
                return True
        except Exception:
            return False

    def validate_tweet(self, text):
        val = re.compile(r"^[a-zA-Z0-9\s\n,'.;]{3,280}$")
        try:
            result = val.search(text)
            if result is None:
                return False
            else:
                return True
        except Exception:
            return False

    def sanizate(self, text):
        try:
            text = ascii(text)
            text = text.replace("\\n", " ")
            text = text.replace("'", "")
            text = text.replace('"', "")
            text = str(text)
            text = text.lower()
            return text
        except Exception:
            return ""
