import os
from datetime import datetime

import tweepy
from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.getenv('TOKEN')

client: tweepy.Client = tweepy.Client(bearer_token=TOKEN)


def get_data(query: str, end_time: datetime, *args) -> tweepy.client.Response:
    tweets: tweepy.client.Response = client.search_recent_tweets(query=query,
                                                                 end_time=end_time,
                                                                 tweet_fields=["created_at", "text", "source",
                                                                               "public_metrics"],
                                                                 user_fields=["name", "username", "location",
                                                                              "verified", "description"],
                                                                 next_token=args,
                                                                 max_results=100,
                                                                 expansions=["author_id"]
                                                                 )
    return tweets
