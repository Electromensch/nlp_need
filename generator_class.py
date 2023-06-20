from util.utils import pad, process_data
from tqdm import tqdm
import numpy as np
from collections import defaultdict
from copy import deepcopy
import re
from collections import Counter


class MarkovChains:
    def __init__(self, n_grams=2, texts=None):
        self.n_grams = n_grams
        self.counter_dict = None
        self.n_tokens = None
        self.vocab = None
        self.inverse_vocab = None
        self.texts = texts
        if not self.texts is None:
            self.counter_dict, self.vocab, self.n_tokens = self.build_vocab()
        self.dict_probs = defaultdict(dict)

    def build_vocab(self):
        if isinstance(self.texts, list):
            vocab = list(set(np.hstack([i.split(' ') for i in self.texts])))
        elif isinstance(self.texts, str):
            vocab = list(set(self.texts.split(' ')))
            self.texts = [pad(i.strip(), '<end>', left=False) for i in self.texts.split('<end>')]
        counter_dict = Counter([])
        for sentence in tqdm(self.texts):
            tokens = sentence.split(' ')
            for l in range(len(tokens) - self.n_grams + 2):
                counter_dict.update([' '.join(tokens[l:l + self.n_grams - 1])])
        n_tokens = len(vocab)
        print('Build vocabulary')
        return counter_dict, vocab, n_tokens

    def train(self, texts=None):
        if texts is None:
            assert self.texts, 'Please provide texts data'
        else:
            self.texts = texts
        if self.vocab is None:
            self.counter_dict, self.vocab, self.n_tokens = self.build_vocab()
        n_gram_counter = Counter([])
        for sentence in tqdm(self.texts):
            tokens = sentence.split(' ')
            for l in range(len(tokens) - self.n_grams + 1):
                n_gram_counter.update([' '.join(tokens[l:l + self.n_grams])])
        for n_gram, freq in tqdm(n_gram_counter.items()):
            tokens = n_gram.split(' ')
            main_token = tokens[-1]
            cond_tokens = ' '.join(tokens[:-1])
            cond_tokens_freq = self.counter_dict[cond_tokens]
            self.dict_probs[cond_tokens][main_token] = freq / cond_tokens_freq
        print('Finished training')

    def generate(self, start_token='<start>', end_token='<end>',
                 decoding='random', beam_size=2, max_sent_size=15):
        if start_token == '<start>':
            start_token2 = [start_token for i in range(self.n_grams - 1)]
            generated_tokens = [' '.join(start_token2)]
            n_seq = 1
        else:
            start_token2 = ['<start>' for i in range(self.n_grams - 2)]
            start_token2.append(start_token)
            generated_tokens = [' '.join(start_token2)]
            n_seq = 2
        if decoding == 'beam_search':
            probs = [[0]]
            sentences = [start_token2]
            while True:
                new_probs = []
                new_sentences = []
                for c, sentence in enumerate(sentences):
                    if len(sentence) <= max_sent_size or sentence[-1] != '<end>':
                        start_token2 = sentence[-self.n_grams + 1:]
                        all_probs = self.dict_probs[' '.join(start_token2)]
                        variants = list(all_probs.keys())
                        all_probs = np.array(list(all_probs.values()))
                        top_words = [variants[i] for i in all_probs.argsort()[-beam_size:]]
                        top_probs = [all_probs[i] for i in all_probs.argsort()[-beam_size:]]

                        new_sentences.extend([sentence + [i] for i in top_words])
                        new_probs.extend([probs[c] + [i] for i in top_probs])
                    else:
                        new_sentences.append(sentence)
                        new_probs.append(probs[c])

                sentences = deepcopy(new_sentences)
                probs = deepcopy(new_probs)

                rules = [len(sentence) >= max_sent_size or sentence[-1] == '<end>' for sentence in sentences]

                if all(rules):
                    break

            idx = np.argmax(np.sum(probs, axis=1))
            sentence = ' '.join(sentences[idx]).replace('<start> ', '').replace('<end>', '')
            sentence += '.'
            return sentence

        else:
            while True:
                generated_tokens = list(np.hstack(i.split(' ') for i in generated_tokens))
                probs = self.dict_probs[' '.join(generated_tokens[-self.n_grams + 1:])]
                variants = list(probs.keys())
                probs = list(probs.values())
                if decoding == 'greedy':
                    idx = np.argmax(probs)
                else:
                    idx = np.random.choice(range(len(variants)), p=probs)
                next_token = variants[idx]
                if next_token == end_token:
                    break
                generated_tokens.append(next_token)
            generated_tokens.append('.')
            generation = ' '.join(generated_tokens[self.n_grams - n_seq:]).capitalize()
            return generation

    def get_params(self):
        return self.dict_probs
