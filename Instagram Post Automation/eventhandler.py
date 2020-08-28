from watchdog.events import FileSystemEventHandler

from post import Post
from setup_ import POST_DAYS, POST_LIST, PASSWORD, USERNAME, DATES_OF_POSTS, DAYS_MAP, POST_HOUR
import os
import json
import datetime
from datetime import timedelta

"""example path"""
path = '/Users/Justin/Documents/IGPhotos/'


def save_post():
    with open('posts.json', 'w') as json_file:
        json.dump(POST_LIST.serialize(), json_file)


def get_next_available_date():
    return_date = datetime.date.today()
    try:
        post = DATES_OF_POSTS['post_' + str(len(POST_LIST.posts)) + ".jpg"]
        return_date = post.post_date + timedelta(days=1)
    except Exception as e:
        print("exception")

    exists = True
    while exists:
        if DAYS_MAP[return_date.weekday()] not in POST_DAYS:
            return_date = return_date + timedelta(days=1)
            print("EXISTS")
        else:
            exists = False
    return return_date


class MyHandler(FileSystemEventHandler):
    i = 1
    new_description = ''

    def on_modified(self, event):
        self.i = 1
        folder_path = '/Users/Justin/Documents/Projects/MyProjects/InstaAutomator/finalized-photos'
        list_of_file_names = []
        for filename in os.listdir(path):
            new_name = str(self.i) + ".jpg"
            exists = True
            while exists:
                file_exists = os.path.isfile(folder_path + '/' + new_name)
                if file_exists:
                    DATES_OF_POSTS[new_name] = POST_LIST.posts[self.i - 1]
                    self.i += 1
                    new_name = str(self.i) + ".jpg"
                else:
                    exists = False

            new_name = folder_path + "/" + new_name
            src = path + "/" + filename
            self.description_added('', src, new_name)

    def description_added(self, description, src, new_name):
        os.rename(src, new_name)
        self.i += 1
        date_of_post = get_next_available_date()
        new_post = Post(description, str(self.i - 1) + ".jpg", date_of_post, False)
        DATES_OF_POSTS[str(self.i - 1) + ".jpg"] = new_post
        POST_LIST.posts.append(new_post)
        save_post()
        try:
            POST_LIST.initialize_posts()
        except FileNotFoundError as e:
            print('no json')
