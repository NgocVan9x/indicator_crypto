# -*- coding: utf-8 -*-
import time
import telebot
import sys
import logging
import os
import os
from Indicators import getData, calculate
from export_image import render_mpl_table
import requests
import json
from api_market import getChatId

API_TOKEN = ''

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_ids = getChatId()
    if message.chat.id not in chat_ids:
        f = open('chat_ids.txt',"a")
        f.write(str(message.chat.id)+'\n')
        f.close()
    msg = bot.reply_to(message, "Added to list")
    bot.register_next_step_handler(msg, send_data_indicator)

def send_data_indicator(message):
    try:
        # params = message.text[3:len(message.text)]
        params=message.text.split(",")
        inputs = getData(params[0],params[1],params[2])
        data = calculate(inputs)
        title=message.text.upper()
        fileName = render_mpl_table(data,title)
        bot.send_photo(chat_id=message.chat.id, photo=open('./'+fileName, 'rb'))
    except Exception as e:
        bot.reply_to(message,"anh ơi anh gõ từ từ thôi anh ")
    finally:
        bot.register_next_step_handler(message, send_data_indicator)

# def main_loop():
while True :
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)