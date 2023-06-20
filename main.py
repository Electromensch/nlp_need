from TelegramBot import TelegramBot
from util.argparse_utils import parse_argss
from generator_class import MarkovChains
import telebot


if __name__ == '__main__':
    args = parse_argss()
    telegrambot = TelegramBot(model='models/model'+ args.ngram_size + 'pkl', decoding=args.decoding_technique)
    telegrambot.start()


