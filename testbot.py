import requests
import json
import schedule
import time
from Indicators import getData, calculate
from export_image import render_mpl_table
from api_market import getChatId

import telebot

API_TOKEN = '659604163:AAEfhonOKmaG1-qyt2Ivlz5oUQ_YaNbBFqo'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_ids = getChatId()
    if message.chat.id not in chat_ids:
        f=open("chat_ids.txt", "r")
        if f.mode == 'r':
          contents =f.read()
        contents+=str(message.chat.id)+'\n'
        f = open('chat_ids.txt','w')
        f.write(contents)
        f.close()
    bot.reply_to(message, "Added to list")

while True :
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)