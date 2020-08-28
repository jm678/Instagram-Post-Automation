import json
from datetime import datetime


class Post:
    def __init__(self, description, image, post_date, posted):
        self.image = image
        self.description = description
        self.post_date = post_date
        self.posted = posted

    def serialize(self):
        date = self.post_date.strftime("%Y-%m-%d %H:%M:%S")
        return {
            'image': self.image,
            'description': self.description,
            'post_date': date,
            'posted': self.posted
        }
