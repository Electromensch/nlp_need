import argparse

def parse_argss():
    parser = argparse.ArgumentParser()
    parser.add_argument('-ngram_size', type=str, help='n_gram_size between 2 and 4', default='2')
    parser.add_argument('-decoding_technique', help='choose one of the decoding techniques (random, greedy, beam_search)',
                        default='random')

    return parser.parse_args()

