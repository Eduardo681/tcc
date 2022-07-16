import nltk
from sklearn.feature_extraction.text import CountVectorizer

from train_classifier import model, vectorizer
from util import *

nltk.download('rslp')
nltk.download('stopwords')
nltk.download('omw-1.4')
nltk.download('wordnet')

# variavel de pesquisa
query_lang: str = "ifood lang:pt"

# df = generate_data_frame(query_lang)
df: pd.DataFrame = pd.read_csv("csvs/analise.csv")
df.info()
print(df.shape)

df_aux: pd.Series = df.value_counts(df['text'])
df_aux.head()

df: pd.DataFrame = pd.DataFrame(df)
df_pre: pd.DataFrame = pre_processing(df)
print(df_pre.shape)

# tokenizacao
tokens_words: list = tokenize(df_pre)
tokens_words = remove_stopwords(tokens_words, query_lang)
tokens_words = generate_lemma(tokens_words)
tokens_words = [word for word in tokens_words if len(word) > 2]

# frequencias
value_of_words: tuple = generate_value_of_words(df_pre, tokens_words)
freq: nltk.probability.FreqDist = nltk.FreqDist(t.lower() for t in tokens_words)

df_frequency: pd.DataFrame = pd.DataFrame(freq.most_common(), columns=['word', 'freq'])
df_likes: pd.DataFrame = pd.DataFrame(list(value_of_words[0].items()), columns=['word', 'likes'])
df_rt: pd.DataFrame = pd.DataFrame(list(value_of_words[1].items()), columns=['word', 'rt'])
df_reply: pd.DataFrame = pd.DataFrame(list(value_of_words[2].items()), columns=['word', 'reply'])
df_quotes: pd.DataFrame = pd.DataFrame(list(value_of_words[3].items()), columns=['word', 'quotes'])

df_frequency_final: pd.DataFrame = pd.merge(df_frequency, df_likes, on='word', how='outer')
df_frequency_final = pd.merge(df_frequency_final, df_rt, on='word', how='outer')
df_frequency_final = pd.merge(df_frequency_final, df_reply, on='word', how='outer')
df_frequency_final = pd.merge(df_frequency_final, df_quotes, on='word', how='outer')

# nuvens de palavras
show_word_cloud(value_of_words[0], "Likes")
show_word_cloud(value_of_words[1], "Compartilhamentos")
show_word_cloud(value_of_words[2], "Comentários")
show_word_cloud(value_of_words[3], "Citações")

# analise de sentimentos
text: list = df_pre['text'].values
freq_text: CountVectorizer = vectorizer.transform(text)
sentiments: list = model.predict(freq_text)
df_pre = df_pre.assign(sentiment=sentiments)
df_positive: pd.DataFrame = df_pre[df_pre['sentiment'] == 'pos']
df_negative: pd.DataFrame = df_pre[df_pre['sentiment'] == 'neg']
countAll = df_pre.shape[0]
countPositive = df_positive.shape[0]
countNegative = df_negative.shape[0]
print(f'Positivos: {countPositive} - {(countPositive / countAll):.2%} ')
print(f'Negativos: {countNegative} - {(countNegative / countAll):.2%} ')

df_frequency_final.to_csv(f"csvs/frequencias.csv")

df_pre.columns = ['id', 'tweet_id', 'Usuário', 'Publicação', 'Data', 'Compartilhamentos', 'Comentários', 'Likes',
                  'Citações', 'Sentimento']
for i in df_pre.index:
    test = df[df['id_tweet'] == (df_pre['tweet_id'][i])]
    df_pre['Publicação'][i] = test['text'].values[0]

df_pre.pop("id")
df_pre.to_csv('csvs/final.csv')
