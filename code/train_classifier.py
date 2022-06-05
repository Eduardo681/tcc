import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_predict
from sklearn.naive_bayes import BernoulliNB

dataset: pd.DataFrame = pd.read_csv('csvs/treino_sentimentos.csv', encoding='utf-8')
dataset['text_pt'] = dataset['text_pt'].fillna("")
dataset['sentiment'] = dataset['sentiment'].fillna("")
text: list = dataset['text_pt'].values

classes: list = dataset['sentiment'].values
vectorizer: CountVectorizer = CountVectorizer(analyzer="word", ngram_range=(1, 2))
freq: list = vectorizer.fit_transform(text)
modelo: BernoulliNB = BernoulliNB()
modelo.fit(freq, classes)

results: list = cross_val_predict(modelo, freq, classes, cv=10)
metrics.accuracy_score(classes, results)
print(metrics.classification_report(classes, results))
