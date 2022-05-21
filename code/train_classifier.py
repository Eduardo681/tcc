import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import cross_val_predict
from sklearn.naive_bayes import MultinomialNB

dataset = pd.read_csv('./csvs/train.csv', encoding='utf-8')
dataset['Text'] = dataset['Text'].fillna("")
dataset['Classificacao'] = dataset['Classificacao'].fillna("Neutro")
tweets = dataset['Text'].values

classes = dataset['Classificacao'].values
vectorizer = CountVectorizer(analyzer="word", ngram_range=(1, 2))
freq_tweets = vectorizer.fit_transform(tweets)
modelo = MultinomialNB()
modelo.fit(freq_tweets, classes)

resultados = cross_val_predict(modelo, freq_tweets, classes, cv=10)
metrics.accuracy_score(classes, resultados)
sentimentos = ["Positivo", "Negativo", "Neutro"]
print(metrics.classification_report(classes, resultados))
