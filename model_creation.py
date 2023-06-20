from generator_class import MarkovChains
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from util.utils import process_data, pad
import pickle


df = pd.read_pickle('mypickle3')
my_gram = 4


df1 = df[df.text == 'Tesak']
df2 = df[df.text == 'Koran'].sample(len(df1), random_state=0)
df_bal = pd.concat([df1, df2])
processed_texts = process_data(df_bal.sentences, n_gram=my_gram)


model4 = MarkovChains(n_grams=my_gram, texts=processed_texts)
model4.train()

with open('models/model4pkl', 'wb') as f:
    pickle.dump(model4, f)



