# -*- coding: utf-8 -*-
import time
import telebot
import sys
import logging
import os
from Indicators import getData
from export_image import render_mpl_table

API_TOKEN = '617289038:AAEFcSERrsI_N65ZHTWu0EapdOGWF5rs4c4'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

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
        title=message.text.upper()
        fileName = render_mpl_table(data,title)
        # bot.reply_to(message, data)
        bot.send_photo(chat_id=message.chat.id, photo=open('./'+fileName, 'rb'))
        os.remove('./'+fileName)
    except Exception as e:
        bot.reply_to(message, 'oooops'+str(e))
    finally:
        bot.register_next_step_handler(message, send_data_indicator)

def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)
if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print >> sys.stderr, '\nExiting by user request.\n'
        sys.exit(0)