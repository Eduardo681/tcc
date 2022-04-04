from util import *

nltk.download('rslp')
nltk.download('stopwords')

# variavel de pesquisa
query_lang: str = "ifood lang:pt"

# df = generate_data_frame(query_lang)
df = pd.read_csv("csvs/ifood_2022-04-02 11:56:53.903762.csv")
df = pd.DataFrame(df)
df = pre_processing(df)
show_word_cloud(df, query_lang)
df_weight = generate_value_of_words(df)
