import os
import re
from datetime import datetime

import matplotlib.pyplot as plt
import nltk
import pandas as pd
import tweepy
from dotenv import load_dotenv
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from unidecode import unidecode
from wordcloud import WordCloud

load_dotenv()

TOKEN: str = os.getenv('TOKEN')

client: tweepy.Client = tweepy.Client(bearer_token=TOKEN)


def get_data(query: str, end_time: datetime, *args) -> tweepy.client.Response:
    """
        Retorna o response da API do twitter para a pesquisa e data informada

        :param query: str
        :param end_time: datetime
        :param args: none
        :return tweets: tweepy.client.Response
    """

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


def generate_data_frame(query_lang: str, limit: int = 10000) -> pd.DataFrame:
    """
    Retorna um dataframe com base na pesquisa informada e o limite de registros, para evitar que tenha que ser executado diversas vezes é armazenado um .csv do dataframe
    :param query_lang: str
    :param limit: int por padrão 10000
    :return: df: pandas.DataFrame
    """

    end_time: datetime = datetime.now()
    data: list[dict] = []
    response: tweepy.client.Response = get_data(query_lang, end_time)
    users: list = response.includes['users']

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
            response = get_data(query_lang, end_time, response.meta["next_token"])
            users = response.includes['users']
        except KeyError:
            break

    df = pd.DataFrame(data)
    df.to_csv(f"csvs/{query_lang.split(' ')[0]}_{end_time}.csv", ",")
    return df


def show_word_cloud(df: pd.DataFrame, query_lang: str):
    """
    Exibe nuvem de palavras a partir de um dataFrame que tenha uma coluna ['text']
    :param query_lang: str
    :param df: pandas.DataFrame
    :return: none
    """
    text = " ".join(item.split()[1] for item in df["text"])
    wordcloud = WordCloud(width=1000, height=1000,
                          background_color='white',
                          stopwords=get_stopwords(query_lang),
                          min_font_size=12).generate(text)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()


def pre_processing(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe um dateFrame e o retorna ele mesmo com a coluna ['text'] pré-processada
    :param data_frame: pandas.DataFrame
    :return: pandas.DataFrame
    """
    df: pd.DataFrame = data_frame

    # converte todas as letras para minúsculo
    df["text"] = df["text"].apply(lambda x: x.lower())

    # remove números e caracteres especiais
    df["text"] = df["text"].apply(lambda x: re.sub('[0-9]|,|\.|/|$|\(|\)|-|\+|:|•', ' ', x))

    # remove acentos
    df["text"] = df["text"].apply(lambda x: unidecode(x))

    # stemming
    stemmer = nltk.stem.RSLPStemmer()
    df["text"] = df["text"].apply(lambda x: stemmer.stem(x))

    # remove textos duplicados
    df = df.drop_duplicates(subset=["text"])

    return df


def get_stopwords(query_lang: str) -> set:
    """
    Gera e retorna a lista de stopwords em pt/br e adiciona a pesquisa a ela
    :param query_lang: str
    :return: set
    """
    stop_words: list = stopwords.words('portuguese')
    stop_words.extend([query_lang.split(" ")[0]])
    return set(stop_words)


def generate_value_of_words(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe um dataframe com uma coluna chamada ['text'] e retorna a matrix de frequencia de cada palavra
    :param df: pd.Dataframe
    :return: pd.Dataframe
    """
    cv: CountVectorizer = CountVectorizer()
    text: str = " ".join(item.split()[1] for item in df["text"])
    word_count_vector: list = cv.fit_transform(text.split(" "))
    tfidf_transformer: TfidfTransformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    df_weight: pd.DataFrame = pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names_out(), columns=["weight"])
    df_weight.sort_values(by=['weight'])
    return df_weight
