import pickle
import re

def unpickles(dirs):
    with open(dirs, 'rb') as f:
        return pickle.load(f)


def pad(x, char, n=1, left=True):
    if left:
        return ' '.join(char for i in range(n)) + " " + x
    else:
        return x + " " + ' '.join(char for i in range(n))



def process_data(x, start_token='<start>', end_token='<end>', lower=False, n_gram=2):
    n_gram = max(n_gram, 2)
    if isinstance(x, str):
        x = re.split(r'[.?!]\s*', x)
    x = [re.sub('[^\w]+', ' ', sentence).strip() for sentence in x]
    if lower:
        x = [sentence.lower() for sentence in x]
    x = [sentence.replace('.', '').replace(',', '').replace('!', '').replace('?', '').strip() for sentence in x if
         sentence]
    x = [pad(sentence, start_token, n_gram - 1, left=True) for sentence in x if sentence]
    x = [pad(sentence, end_token, 1, left=False) for sentence in x if sentence]
    return x