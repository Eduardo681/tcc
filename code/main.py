import nltk
import pandas as pd
import spacy.cli

from util import *

# nltk.download('rslp')
# nltk.download('stopwords')
# nltk.download('omw-1.4')
# nltk.download('wordnet')
# spacy.cli.download('pt_core_news_lg')

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

tokens_words = tokenize(df)
tokens_words = remove_stopwords(tokens_words, query_lang)
tokens_words = generate_lemma(tokens_words)
tokens_words = [word for word in tokens_words if len(word) > 2]

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

show_word_cloud(value_of_words[0], "Likes")
show_word_cloud(value_of_words[1], "RT")
show_word_cloud(value_of_words[2], "Reply")
show_word_cloud(value_of_words[3], "Quotes")
