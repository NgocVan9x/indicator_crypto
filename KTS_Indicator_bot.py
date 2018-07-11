# -*- coding: utf-8 -*-
import time
import telebot
import sys
import logging
import os
from Indicators import getData, calculate
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
        inputs = getData(params[0],params[1],params[2])
        data = calculate(inputs)
        title=message.text.upper()
        fileName = render_mpl_table(data,title)
        # bot.reply_to(message, data)
        bot.send_photo(chat_id=message.chat.id, photo=open('./'+fileName, 'rb'))
        # os.remove('./'+fileName)
    except Exception as e:
        bot.reply_to(message, 'oooops '+"anh ơi anh gõ từ từ thôi anh "+str(e))
    finally:
        bot.register_next_step_handler(message, send_data_indicator)

# def main_loop():
while True :
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)