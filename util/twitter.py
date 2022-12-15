import tweepy

from credentials import TWITTER_BEARER_TOKEN, TWITTER_API_KEY, TWITTER_API_KEY_SECRET
from util import CommentData

client = tweepy.Client(TWITTER_BEARER_TOKEN, wait_on_rate_limit=True)


def get_twitter_replies(conversation_id: str):  # -> dict[str, CommentData]:
    for response in tweepy.Paginator(client.search_recent_tweets, query=f"conversation_id:{conversation_id}", max_results=100).flatten():
        print(response)
