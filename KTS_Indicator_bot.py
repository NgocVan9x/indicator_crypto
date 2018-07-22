# -*- coding: utf-8 -*-
import time
from common import getBot, getDataAndSendBot, getChatId

bot = getBot()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_ids = getChatId()
    if message.chat.id not in chat_ids:
        f = open('chat_ids.txt', "a")
        f.write(str(message.chat.id)+'\n')
        f.close()
    msg = bot.reply_to(message, "Added to list")
    bot.register_next_step_handler(msg, send_data_indicator)


def send_data_indicator(message):
    try:
        # params = message.text[3:len(message.text)]
        params = message.text.split(",")
        chat_ids = getChatId()
        fileName = "data_manual_image.png"
        getDataAndSendBot("From manual", fileName,
                          chat_ids, params[0], params[1], params[2])
    except Exception as e:
        bot.reply_to(message, "anh ơi anh gõ từ từ thôi anh ")
    finally:
        bot.register_next_step_handler(message, send_data_indicator)


# def main_loop():
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
