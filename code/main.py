from util import *

df = generate_data_frame()
df = df.drop_duplicates(subset=["text"])

show_word_cloud(df)
