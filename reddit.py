import praw
import requests
from config import REDDIT_SECRET, REDDIT_USER_AGENT, REDDIT_ID


class RedditNews:
    def __init__(self, title, url, shortlink, thumbnail):
        self.title = title
        self.url = url
        self.shortlink = shortlink
        self.thumbnail = thumbnail


def reddit_french_sub():
    exept = 'self', 'default', 'nsfw'
    reddit = praw.Reddit(
        client_id=REDDIT_ID,
        client_secret=REDDIT_SECRET,
        user_agent=REDDIT_USER_AGENT,
    )
    reddit_fr = []

    for red in reddit.subreddit("france").new(limit=10):
        if red.thumbnail in exept:
            thumb = None
        else:
            thumb = requests.get(red.thumbnail).content

        reddit_fr.append(RedditNews(red.title, red.url, red.shortlink, thumb))
        continue

    return reddit_fr
