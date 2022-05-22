import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_predict
from sklearn.naive_bayes import BernoulliNB

dataset: pd.DataFrame = pd.read_csv('./csvs/imdb-reviews-pt-br.csv', encoding='utf-8')
dataset['text_pt'] = dataset['text_pt'].fillna("")
dataset['sentiment'] = dataset['sentiment'].fillna("")
tweets: list = dataset['text_pt'].values

classes: list = dataset['sentiment'].values
vectorizer: CountVectorizer = CountVectorizer(analyzer="word", ngram_range=(1, 2))
freq_tweets: list = vectorizer.fit_transform(tweets)
modelo: BernoulliNB = BernoulliNB()
modelo.fit(freq_tweets, classes)

results: list = cross_val_predict(modelo, freq_tweets, classes, cv=10)
metrics.accuracy_score(classes, results)
sentiments: list = ["neg", "pos"]
print(metrics.classification_report(classes, results))
