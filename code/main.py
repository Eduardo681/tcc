import os

import tweepy
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
query = "#magalu lang:pt -is:retweet"

start_time = "2022-03-08T00:00:00Z"
end_time = "2022-03-09T00:00:00Z"

client = tweepy.Client(bearer_token=TOKEN)

tweets = client.search_recent_tweets(query=query,
                                     start_time=start_time,
                                     end_time=end_time,
                                     tweet_fields=["created_at", "text", "source"],
                                     user_fields=["name", "username", "location", "verified", "description"],
                                     max_results=10,
                                     expansions='author_id'
                                     )
print(tweets)