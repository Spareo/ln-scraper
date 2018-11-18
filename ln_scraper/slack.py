
import requests

class Message(object):
    def __init__(self, title, text, emoji=None, attachments=None):
        self.title = title
        self.attachments = attachments
        self.text = text
        self.emoji = emoji

    def to_dict(self):
        d = {
            "title": self.title,
            "attachments": [a.to_dict() for a in self.attachments]
        }
        if self.text:
            d["text"] = self.text
        if self.emoji:
            d["icon_emoji"] = self.emoji
        return d

    def send(self, url, username=None, channel=None):
        d = self.to_dict()

        if channel:
            d["channel"] = channel
        if username:
            d["username"] = username

        requests.post(url, json=d)

class Field(object):
    def __init__(self, title, value, short=True):
        self.title = title
        self.value = value
        self.short = short

    def to_dict(self):
        return {
            "title": self.title,
            "value": self.value,
            "short": self.short
        }

class Attachment(object):
    def __init__(self, title, color, text=None, fields=None, image_url=None):
        self.title = title
        self.color = color
        self.text = text
        self.fields = fields
        self.image_url = image_url

    @property
    def fallback(self):
        if self.text:
            return "{}: {}".format(self.title, self.text)
        else:
            return "New property scrapped from LoopNet!"

    def to_dict(self):
        d = {
            "title": self.title,
            "fallback": self.fallback,
            "color": self.color,
            "image_url": self.image_url
        }
        if self.text:
            d["text"] = self.text
        if self.fields:
            d["fields"] = [f.to_dict() for f in self.fields]
        return d