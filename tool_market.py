import requests
import schedule
import time
from common import getBot, getChatId, getDataAndSendBotTool, getPriceDataBinance
from datetime import datetime
from pytz import timezone

bot = getBot()

list_coin = []

added_listcoin = False

def getDataFromBinance():
    prices = getPriceDataBinance()
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    now_utc = datetime.utcnow()
    chat_ids = getChatId()
    global added_listcoin, list_coin
    if added_listcoin:
        del list_coin[:]
    
    #send stated
    for chat_id in chat_ids:
        bot.send_message(
            chat_id, "Start Scan List Coin Time UTC " + now_utc.strftime(fmt))
    print(added_listcoin, list_coin)
    for price in prices:
        if price["symbol"][-3:] == "SDT" or price["symbol"][-3:] == "BTC" and price["symbol"] not in list_coin:
            coin = getDataAndSendBotTool(chat_ids, price["symbol"])
            if coin is not None:
                list_coin.append(coin)
    # global added_listcoin
    added_listcoin = not added_listcoin
    print(added_listcoin, list_coin)
    return prices

if __name__ == '__main__':
    schedule.every(1).minutes.do(getDataFromBinance)
    # getDataFromBinance()
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(15)
