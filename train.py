import argparse

def parse_argss():
    parser = argparse.ArgumentParser()

    parser.add_argument('-ngram_size', type=str, help='n_gram_size between 2 and 4', default='2')
    parser.add_argument('-decoding_technique', help='choose one of the decoding techniques (random, greedy, beam_search)',
                        default='random')

    return parser.parse_args()

args = parse_argss()

#if args.ngram_size in ['2', "3" , '4']:
#    print(args.ngram_size)

print(args.encoding_technique)
