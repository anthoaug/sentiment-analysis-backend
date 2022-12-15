import tweepy

from credentials import TWITTER_BEARER_TOKEN
from util import CommentData

client = tweepy.Client(TWITTER_BEARER_TOKEN, wait_on_rate_limit=True)


def get_twitter_replies(tweet_id: str):
    conversation_id = client.get_tweet(id=tweet_id, tweet_fields='conversation_id').data['conversation_id']

    for response in tweepy.Paginator(client.search_recent_tweets, query=f"conversation_id:{conversation_id}", max_results=100).flatten():
        print(response)
