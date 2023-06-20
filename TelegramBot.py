import telebot
import pickle
from util.utils import unpickles, pad
from telebot import types
import generator_class
import logging

logger=telebot.logger
telebot.logger.setLevel(logging.DEBUG)

class TelegramBot:
    TOKEN = '5689651802:AAEmpFPX8Cgj9DX56VEJVAG-TtYEXlZ0L9w'

    BOT = telebot.TeleBot(TOKEN)

    def __init__(self, model='models/model2pkl',
                 start_token='<start>',
                 decoding='random',
                 beams_size=2,
                 max_sent_size=15):
        self.model = unpickles(model)
        self.start_token = start_token
        self.decoding = decoding
        self.beams_size = beams_size
        self.max_sent_size = max_sent_size

        print('launched')

        @self.BOT.message_handler(content_types=['text'])
        def reply(message):

            welcome_text = f"Hi {message.from_user.first_name}, \nI'm rofl-sentence generator. To generate sentence use command /generate." \
                           f"You can choose some parameters or generate sentence with default ones." \
                           f"To see current parameters use /parameters command. Choose n_gram size"

            if message.text == "/help":
                self.BOT.send_message(message.from_user.id,
                                      "In order to start the bot please write /start.")

            elif message.text == '/start':

                ngram = types.InlineKeyboardMarkup(row_width=3)
                item1 = types.InlineKeyboardButton('n_gram=2', callback_data='n_gram=2')
                item2 = types.InlineKeyboardButton('n_gram=3', callback_data='n_gram=3')
                item3 = types.InlineKeyboardButton('n_gram=4', callback_data='n_gram=4')
                ngram.add(item1, item2, item3)
                self.BOT.send_message(message.chat.id, welcome_text, reply_markup=ngram)

            elif message.text == '/set_default':
                self.model = unpickles('models/model2pkl')
                self.start_token = '<start>'
                self.decoding = 'random'
                self.beams_size = 2
                self.max_sent_size = 15

            elif message.text.startswith('/update'):
                text_params = types.InlineKeyboardMarkup(row_width=3)
                param1 = types.InlineKeyboardButton('start_token', callback_data='start_token')
                param2 = types.InlineKeyboardButton('decoding', callback_data='decoding')
                param3 = types.InlineKeyboardButton('beams_size', callback_data='beams_size')
                param4 = types.InlineKeyboardButton('max_sent_size', callback_data='max_sent_size')
                text_params.add(param1, param2, param3, param4)
                self.BOT.send_message(message.chat.id, welcome_text, reply_markup=text_params)

            elif message.text == '/parameters':
                self.BOT.send_message(message.chat.id,
                    text= f'start_token = {self.start_token}, decoding = {self.decoding}, beams_size = {self.beams_size}, max_sent_size = {self.max_sent_size}' \
                                      .replace('<start>', 'any')
                                      )

            elif message.text == '/generate':
                try:
                    self.BOT.send_message(message.from_user.id,
                                      self.model.generate(start_token=self.start_token, decoding=self.decoding,
                                                            beam_size=self.beams_size, max_sent_size=self.max_sent_size)
                                      )
                except ValueError:
                    self.BOT.send_message(message.chat.id, 'Please change start token')

            elif len(message.text.split()) != 1:
                self.BOT.send_message(message.from_user.id, 'dovboyob?'
                                     )

            else:
                if message.text.isnumeric():
                    self.max_sent_size = int(message.text)
                    self.BOT.send_message(message.chat.id, 'You have changed max sentence size')
                else:
                    self.start_token = message.text
                    self.BOT.send_message(message.chat.id, 'You have changed start token')

            logger.debug(message)

        @self.BOT.callback_query_handler(func=lambda callback: callback.data)
        def callback_inline(callback):
            if callback.data in ['n_gram=2', 'n_gram=3', 'n_gram=4']:
                self.model = unpickles('models/model' + str(callback.data[-1]) + 'pkl')
                self.BOT.send_message(callback.message.chat.id, 'Use /update to update other parameters')
            elif callback.data == 'start_token':
                self.BOT.send_message(callback.message.chat.id, 'Type a word')
            elif callback.data == 'decoding':
                dec_params = types.InlineKeyboardMarkup(row_width=2)
                dec1 = types.InlineKeyboardButton('random', callback_data='random')
                dec2 = types.InlineKeyboardButton('beam search', callback_data='beam_search')
                dec3 = types.InlineKeyboardButton('greedy', callback_data='greedy')
                dec_params.add(dec1, dec2, dec3)
                self.BOT.send_message(callback.message.chat.id, 'Choose decoding technique', reply_markup=dec_params)
            elif callback.data in ['random', 'beam_search', 'greedy']:
                self.decoding = callback.data

            elif callback.data == 'beams_size':
                bs_params = types.InlineKeyboardMarkup(row_width=3)
                bs1 = types.InlineKeyboardButton('2', callback_data='bs2')
                bs2 = types.InlineKeyboardButton('3', callback_data='bs3')
                bs3 = types.InlineKeyboardButton('4', callback_data='bs4')

                bs_params.add(bs1, bs2, bs3)
                self.BOT.send_message(callback.message.chat.id, 'Choose number', reply_markup=bs_params)
            elif callback.data in ['bs2', 'bs3', 'bs4']:
                self.beams_size = int(callback.data[-1])
            elif callback.data == 'max_sent_size':
                self.BOT.send_message(callback.message.chat.id, 'Type whole number')

    def start(self):
        self.BOT.polling(timeout=300)



