from functools import lru_cache

import praw
from redditreview.core.config import settings


@lru_cache(maxsize=1)
def reddit_client():
    reddit = praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET,
        user_agent=settings.REDDIT_USER_AGENT,
    )
    return reddit
