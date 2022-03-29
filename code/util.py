import os
from datetime import datetime

import pandas as pd
import tweepy
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from dotenv import load_dotenv
from ntlk.corpus import stopwords
stop_words = stopwords.words('portuguese')

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


def generate_word_cloud(df: pd.DataFrame):
    text = " ".join(item.split()[1] for item in df["text"])
    wordcloud = WordCloud(width=1000, height=1000,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=8).generate(text)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.tight_layout(pad=0)
    plt.show()

def generate_data_frame() -> pd.DataFrame:
    end_time: datetime = datetime.now()
    query: str = "rappi lang:pt"
    data: list[dict] = []
    response: tweepy.client.Response = get_data(query, end_time)
    users: list = response.includes['users']
    limit: int = 20000

    while len(data) <= limit:
        for user, tweet in zip(users, response.data):
            row: dict = {
                "user": user.name,
                "text": tweet.text,
                "created_at": tweet.created_at,
                "retweet_count": tweet.public_metrics["retweet_count"],
                "reply_count": tweet.public_metrics["reply_count"],
                "like_count": tweet.public_metrics["like_count"],
                "quote_count": tweet.public_metrics["quote_count"],
            }
            data.append(row)

        try:
            response = get_data(query, end_time, response.meta["next_token"])
            users = response.includes['users']
        except KeyError:
            break

    df = pd.DataFrame(data)
    return df