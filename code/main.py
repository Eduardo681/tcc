import nltk
import spacy.cli

from util import *
import dash

import dash_core_components as dcc

import dash_html_components as html

import pandas as pd

nltk.download('rslp')
nltk.download('stopwords')
nltk.download('omw-1.4')
nltk.download('wordnet')
spacy.cli.download('pt_core_news_lg')

# variavel de pesquisa
query_lang: str = "ifood lang:pt"

# df = generate_data_frame(query_lang)
df = pd.read_csv("csvs/ifood_2022-04-15_14:20:31.927856.csv")
df.info()
print(df.shape)

df_aux = df.value_counts(df['text'])
df_aux.head()

df = pd.DataFrame(df)
df = pre_processing(df)
print(df.shape)

# tokenizacao
tokens_words = tokenize(df)
tokens_words = remove_stopwords(tokens_words, query_lang)
tokens_words = generate_lemma(tokens_words)
tokens_words = [word for word in tokens_words if len(word) > 2]

# frequencias
value_of_words: tuple = generate_value_of_words(df, tokens_words)
freq: nltk.probability.FreqDist = nltk.FreqDist(t.lower() for t in tokens_words)

df_frequency: pd.DataFrame = pd.DataFrame(freq.most_common(), columns=['word', 'freq'])
df_likes: pd.DataFrame = pd.DataFrame(list(value_of_words[0].items()), columns=['word', 'likes'])
df_rt: pd.DataFrame = pd.DataFrame(list(value_of_words[1].items()), columns=['word', 'rt'])
df_reply: pd.DataFrame = pd.DataFrame(list(value_of_words[2].items()), columns=['word', 'reply'])
df_quotes: pd.DataFrame = pd.DataFrame(list(value_of_words[3].items()), columns=['word', 'quotes'])

df_frequency_final = pd.merge(df_frequency, df_likes, on='word', how='outer')
df_frequency_final = pd.merge(df_frequency_final, df_rt, on='word', how='outer')
df_frequency_final = pd.merge(df_frequency_final, df_reply, on='word', how='outer')
df_frequency_final = pd.merge(df_frequency_final, df_quotes, on='word', how='outer')

# nuvens de palavras
show_word_cloud(value_of_words[0], "Likes")
show_word_cloud(value_of_words[1], "RT")
show_word_cloud(value_of_words[2], "Reply")
show_word_cloud(value_of_words[3], "Quotes")

df["created_at"] = pd.to_datetime(df["created_at"], format="%Y-%m-%d")

df.sort_values("created_at", inplace=True)

app = dash.Dash(__name__)

app.layout = html.Div(

    children=[

        html.H1(children="Analise de dados nos negocios: aplicação na estrategia de marketing digital", ),

        html.P(

            children="Baseado em dados do twitter",

        ),

        dcc.Graph(

            figure={

                "data": [

                    {

                        "x": df_frequency_final['word'],

                        "y": df_frequency_final['likes'],

                        "type": "bar",

                    },

                ],

                "layout": {"title": "Word vs Likes"},

            },

        ),
    ]

)

if __name__ == "__main__":
    app.run_server(debug=False)
