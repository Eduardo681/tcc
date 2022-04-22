import nltk

from util import *

nltk.download('rslp')
nltk.download('stopwords')

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

freq = nltk.FreqDist(t.lower() for t in tokens_words)
df_frequency = pd.DataFrame(freq.most_common())

value_of_words: tuple = generate_value_of_words(df, query_lang)

show_word_cloud(value_of_words[0], "Likes")
show_word_cloud(value_of_words[1], "RT")
show_word_cloud(value_of_words[2], "Reply")
show_word_cloud(value_of_words[3], "Quotes")
