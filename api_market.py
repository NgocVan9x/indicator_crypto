import requests
import json
import schedule
import time
from Indicators import getData, calculate
from export_image import render_mpl_table
import telebot
from datetime import datetime
from pytz import timezone
import os

API_TOKEN = '606110477:AAGWe3zrCNb7P5QObt6qUsKLq_XuA0k4y0Y'

bot = telebot.TeleBot(API_TOKEN)

def getChatId():
    array = []
    if os.path.exists("myfile.dat"):
        with open("chat_ids.txt", "r") as ins:
            for line in ins:
                if line[0].isdigit():
                    array.append(int(line))
    else:
     f = open('chat_ids.txt','w')
     f.write('')
     f.close()
    return array

def getDataFromBinance():
    headers = {
            "Accept": "application/json",
        }
    url = 'https://api.binance.com/api/v3/ticker/price'
    params={}
    response = requests.get(url=url,params=params,headers=headers)
    prices = response.json()
    
    chat_ids = getChatId()
    for price in prices:
      getDataAndSendBot(chat_ids,price)
    return prices

def getDataAndSendBot(chat_ids, price, interval_stand = '4h',market = 'binance'):
    inputs =  getData(price["symbol"],interval_stand,market)
    data = calculate(inputs)
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    now_utc = datetime.now(timezone('Asia/Bangkok'))
    if int(data['Number'][len(data['Number'])-1]) > 0:
        title = price["symbol"].upper()+" "+interval_stand.upper()+" "+ market.upper()
        fileName =  render_mpl_table(data,title)
        for chat_id in chat_ids:
           bot.send_message(chat_id, "Current time " + now_utc.strftime(fmt))
           bot.send_photo(chat_id=chat_id, photo=open('./'+fileName, 'rb'))

# if __name__ == '__main__':
#     # getDataFromBinance()
#     f=open("chat_ids.txt", "r")
#     if f.mode == 'r':
#       contents =f.read()
#       print(contents)
schedule.every(30).minutes.do(getDataFromBinance)
while True :
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(15)