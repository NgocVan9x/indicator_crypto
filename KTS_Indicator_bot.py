# -*- coding: utf-8 -*-
"""
This Example will show you how to use register_next_step handler.
"""
import time
import telebot
# from telebot import types
from Indicators import *

API_TOKEN = '617289038:AAEFcSERrsI_N65ZHTWu0EapdOGWF5rs4c4'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}


class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = bot.reply_to(message, "Add to list")
    bot.register_next_step_handler(msg, send_data_indicator)

def send_data_indicator(message):
    try:
        # params = message.text[3:len(message.text)]
        params=message.text.split(",")
        data = getData(params[0],params[1],params[2])
        bot.reply_to(message, data)
    except Exception as e:
        bot.reply_to(message, 'oooops'+str(e))
    finally:
        bot.register_next_step_handler(message, send_data_indicator)

bot.polling()