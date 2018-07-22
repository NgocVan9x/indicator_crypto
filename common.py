import telebot
from Indicators import getData, calculate
from export_image import render_mpl_table
import os
import requests

API_TOKEN = ''

bot = telebot.TeleBot(API_TOKEN)


def getDataAndSendBot(title, fileName, chat_ids, symbol, interval_stand, market):
    inputs = getData(symbol, interval_stand, market)
    data = calculate(inputs)
    title += " "+symbol.upper()+" "+interval_stand.upper() + " " + market.upper()
    render_mpl_table(data, title, fileName)
    for chat_id in chat_ids:
        bot.send_photo(chat_id=chat_id, photo=open('./'+fileName, 'rb'))

def getChatId():
    array = []
    if os.path.exists("chat_ids.txt"):
        with open("chat_ids.txt", "r") as ins:
            for line in ins:
                if line[0].isdigit():
                    array.append(int(line))
    else:
        f = open('chat_ids.txt', 'w')
        f.write('')
        f.close()
    return array

def getDataAndSendBotTool(chat_ids, symbol, interval_stand='4h', market='binance'):
    inputs = getData(symbol, interval_stand, market)
    data = calculate(inputs)
    if int(data['oversell']) > 0 and data['macd_sell']:
        title = symbol.upper()+" "+interval_stand.upper()+" " + market.upper()
        fileName = 'data_tool_image.png'
        render_mpl_table(data, title, fileName)
        for chat_id in chat_ids:
            bot.send_photo(chat_id=chat_id, photo=open('./'+fileName, 'rb'))
        return symbol
    return None

def getPriceDataBinance():
    headers = {
        "Accept": "application/json",
    }
    url = 'https://api.binance.com/api/v3/ticker/price'
    params = {}
    response = requests.get(url=url, params=params, headers=headers)
    return response.json()

def getBot():
    return bot