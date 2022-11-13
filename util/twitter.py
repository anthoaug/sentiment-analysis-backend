# import searchtweets
import pandas
import os

# from credentials import TWITTER_BEARER_TOKEN, TWITTER_API_KEY, TWITTER_API_KEY_SECRET
# from searchtweets import load_credentials
from util import CommentData

# os.environ["SEARCHTWEETS_ENDPOINT"] = ...
# os.environ["SEARCHTWEETS_BEARER_TOKEN"] = TWITTER_BEARER_TOKEN
# os.environ["SEARCHTWEETS_CONSUMER_KEY"] = TWITTER_API_KEY
# os.environ["SEARCHTWEETS_CONSUMER_SECRET"] = TWITTER_API_KEY_SECRET
#
# credentials = load_credentials()


def get_twitter_replies(conversation_id: str) -> dict[str, CommentData]:
    pass
