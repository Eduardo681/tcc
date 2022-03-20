import datetime
import tweepy
import pandas as pd
from util import get_data
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

end_time: datetime = datetime.datetime.now()
query: str = "rappi lang:pt"
data: list[dict] = []
response: tweepy.client.Response = get_data(query, end_time)
users: list = response.includes['users']
limit: int = 20000
stopwords: set = set(STOPWORDS)

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
df = df.drop_duplicates(subset=["text"])
text = " ".join(item.split()[1] for item in df["text"])
wordcloud = WordCloud(width=1000, height=1000,
                      background_color='white',
                      stopwords=stopwords,
                      min_font_size=8).generate(text)

plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.tight_layout(pad=0)
plt.show()
