import os
import re
import string
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import tweepy
from dotenv import load_dotenv
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from wordcloud import WordCloud
import spacy

# spacy.cli.download('pt_core_news_lg')
nlp = spacy.load("pt_core_news_lg")

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
                                                                               "public_metrics", "id"],
                                                                 user_fields=["name", "username", "location",
                                                                              "verified", "description"],
                                                                 next_token=args,
                                                                 max_results=100,
                                                                 expansions=["author_id"]
                                                                 )
    return tweets


def generate_data_frame(query_lang: str, limit: int = 10000) -> pd.DataFrame:
    """
        Retorna um dataframe com base na pesquisa informada e o limite de registros, para evitar que tenha que
        ser executado diversas vezes é armazenado um .csv do dataframe
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
                "id_tweet": tweet.id,
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

    df: pd.DataFrame = pd.DataFrame(data)
    df.to_csv(f"csvs/{query_lang.split(' ')[0]}_{end_time}.csv", ",")
    return df


def show_word_cloud(value_frequency: dict, text: str) -> None:
    """
    Gera uma nuvem de palavras com base na frequencia informada no dict
    :param value_frequency: dict
    :param text: str
    :return: None
    """
    wordcloud = WordCloud(width=1000, height=1000,
                          background_color='#0e1012',
                          stopwords=None,
                          min_font_size=12).generate_from_frequencies(value_frequency)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.title(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(w_pad=0)
    plt.show()
    wordcloud.to_file("dash/assets/" + text + ".png")


def pre_processing(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Recebe um dateFrame e o retorna ele mesmo pré-processado
    :param data_frame: pandas.DataFrame
    :return: pandas.DataFrame
    """
    df: pd.DataFrame = data_frame

    # converte todas as letras para minúsculo
    df["text"] = df["text"].apply(lambda x: x.lower())

    # remove números e caracteres especiais
    df["text"] = df["text"].apply(lambda x: re.sub('[0-9]|,|\.|/|\(|\)|-|\+|:|•|\$', ' ', x))

    # remove acentos
    df["text"] = df["text"].apply(
        lambda x: ' '.join([word for word in x.split() if word not in string.punctuation]))

    # remove textos duplicados
    df = df.drop_duplicates(subset=["text"])

    # remove coluna id
    df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1)

    return df


def tokenize(df: pd.DataFrame) -> list[str]:
    """
    Retorna coluna 'text' do dataframe tokenizada em uma lista de palavras
    :param df: pd.DataFrame
    :return: list[str]
    """
    tokenizer: RegexpTokenizer = RegexpTokenizer(r'[A-z]\w*')
    tokens: list[str] = tokenizer.tokenize(df['text'].to_string())
    return tokens


def generate_value_of_words(df: pd.DataFrame, query_lang) -> tuple:
    """
    Recebe um dataframe com uma coluna chamada ['text'] e retorna a uma tupla com
    as palavras e seus pesos levando em consideração outros atributos do df
    :param query_lang: str
    :param df: pd.Dataframe
    :return: tuple
    """
    value_word_likes: dict[str: float] = {}
    value_word_rt: dict[str: float] = {}
    value_word_reply: dict[str: float] = {}
    value_word_quote: dict[str: float] = {}
    for i in df.index:
        for word in nlp(df['text'][i]):
            word = str(word.lemma_)
            if word in query_lang:
                if value_word_likes.get(word) is None:
                    value_word_likes[word] = df['like_count'][i]
                    value_word_rt[word] = df['retweet_count'][i]
                    value_word_reply[word] = df['reply_count'][i]
                    value_word_quote[word] = df['quote_count'][i]
                else:
                    rt, likes, reply, quote = value_word_rt.get(word), value_word_likes.get(word), value_word_reply.get(
                        word), value_word_quote.get(word)
                    value_word_likes[word] = df['like_count'][i] + likes
                    value_word_rt[word] = df['retweet_count'][i] + rt
                    value_word_reply[word] = df['reply_count'][i] + reply
                    value_word_quote[word] = df['quote_count'][i] + quote
    return value_word_likes, value_word_rt, value_word_reply, value_word_quote


def remove_stopwords(list_words: list[str], query_lang: str) -> list[str]:
    """
    Retorna lista de palavras sem as stopwords
    :param list_words: list[str]
    :param query_lang: str
    :return: list[str]
    """
    tokens_without_sw: list[str] = [word for word in list_words if word not in get_stopwords(query_lang)]
    return tokens_without_sw


def get_stopwords(query_lang: str) -> list[str]:
    """
    Retorna lista de stopwords incluindo o termo de pesquisa
    :param query_lang: str
    :return: list[str]
    """
    stop_words: list[str] = stopwords.words('portuguese')
    stop_words.append('rt')
    stop_words.append('pra')
    stop_words.append('https')
    stop_words.append(query_lang.split(' ')[0])
    return stop_words


def generate_lemma(list_words: list[str]) -> list[str]:
    """
    Recebe uma lista de palavras e retorna nova lista, unindo as palavras similares com o seu lemma
    :param list_words:list[str]
    :return: list[str]
    """
    list_lemma: list[str] = []
    for word in nlp(' '.join(list_words)):
        list_lemma.append(word.lemma_)
    return list_lemma
