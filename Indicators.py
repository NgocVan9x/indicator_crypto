import numpy
from talib.abstract import *
import requests
import json

def to_str(var):
    return str(list(numpy.reshape(numpy.asarray(var), (1, numpy.size(var)))[0]))[1:-1]

interval_stand={
  "1m":60,
  "3m":180,
  "5m":300,
  "15m":900,
	"30m":1800,
	"1h":3600,
	"2h":7200,
	"4h":14400,
	"6h":21600,
	"12h":43200,
	"1d":86400,
	"3d":259200,
	"1w":604800,
}
def getInteval(var):
  return interval_stand[var]

def calculate(inputs):
  count_buy = 0
  count_sell = 0
  count_neutural = 0
  count_over_sell = 0
   # print(arr_close[-1])
  rsi_stand=50
  sma10_stand=10
  adx_stand=20
  wr_stand=-45
  uo_stand=10
  roc_stand=0
  ema5_stand=inputs['close'][-1]
  ema10_stand=inputs['close'][-1]
  ema20_stand=inputs['close'][-1]
  ema50_stand=inputs['close'][-1]
  ema100_stand=inputs['close'][-1]
  ema200_stand=inputs['close'][-1]
  sma5_stand=inputs['close'][-1]
  sma10_stand=inputs['close'][-1]
  sma20_stand=inputs['close'][-1]
  sma50_stand=inputs['close'][-1]
  sma100_stand=inputs['close'][-1]
  sma200_stand=inputs['close'][-1]
  atr_stand=inputs['close'][-1]*0.1
  cci_stand=0
  results={}
  results['Number']=[]
  results['Type']=[]
  results['Type'].append(to_str(round(inputs['close'][-1], 6)))
  results['Number'].append(to_str(round(inputs['close'][-1], 6)))
  results['Type'].append('-')
  results['Number'].append("-")

  #####   Calculate RSI(14) and print to console    --> DONE    #####  
  # print ("########    RSI(14)    ##########")
  real = RSI(inputs, timeperiod=14)
  ## count
  if numpy.isnan(real[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if real[-1] > rsi_stand and real[-1] <70:
      count_buy += 1
      if real[-1] >60:
        results['Type'].append('Strong Buy')
      else:
        results['Type'].append('Buy')
    elif real[-1] >70:
      count_neutural +=1
      results['Type'].append('Overbought')
    elif real[-1] == rsi_stand:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      if real[-1]<40 and real[-1]>30:
        results['Type'].append('Strong Sell')
      elif real[-1]<30:
        results['Type'].append('Over Sell')
        count_over_sell+=1
      else:
        results['Type'].append('Sell')
  results['Number'].append(to_str(round(real[-1], 6)))

  #### Calculate STOCH(9,6) and print to console     --> IN PROGRESS    #####
  slowk, slowd = STOCH(inputs,fastk_period=9, slowk_period=6, slowk_matype=0, slowd_period=6, slowd_matype=0)
  if numpy.isnan(slowk[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if slowk[-1] > 55 and slowk[-1] <80:
      count_buy += 1
      if slowk[-1] >60:
        results['Type'].append('Strong Buy')
      else:
        results['Type'].append('Buy')
    elif slowk[-1] >80:
      count_neutural +=1
      results['Type'].append('Overbought')
    elif slowk[-1] < 55 and slowk[-1]>45:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      if slowk[-1]<45 and slowk[-1] > 40:
        results['Type'].append('Sell')
      if slowk[-1]<40 and slowk[-1]>20:
        results['Type'].append('Strong Sell')
      elif slowk[-1]<20:
        results['Type'].append('Over Sell')
        count_over_sell+=1
      # else:
      #   results['Type'].append('Sell')
  # results['Number'].append(to_str(round(real[-1], 6)))
  results['Number'].append(to_str(round(slowk[-1],3))+"--"+to_str(round(slowd[-1],3)))
  # results['Type'].append('-')
  #### Calculate STOCHRSI(14) and print to console     --> IN PROGRESS    #####
  fastk, fastd = STOCHRSI(inputs, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
  results['Number'].append(to_str(round(fastk[-1],3))+"--"+to_str(round(fastd[-1],3)))
  results['Type'].append('-')
  #### Calculate MACD(12,26,9) and print to console     --> IN PROGRESS    #####
  macd, macdsignal, macdhist = MACD(inputs, fastperiod=12, slowperiod=26, signalperiod=9)
  if numpy.isnan(macdsignal[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if macd[-1] >macdsignal[-1]:
      count_buy += 1
      if macdsignal[-1] >=0 and macd[-1] >=0:
        results['Type'].append('Strong Buy')
      else:
        results['Type'].append('Buy')
    elif macdsignal[-1] == macd[-1]:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      if macdsignal[-1] <0 and macd[-1] <0:
        results['Type'].append('Strong Sell')
      else:
        results['Type'].append('Sell')
  results['Number'].append(to_str(round(macd[-1],4))+"  "+to_str(round(macdsignal[-1],4))+"  "+to_str(round(macdhist[-1],4)))
  # results['Type'].append('-')
  #### Calculate ADX(14) and print to console    --> DONE    #####
  adx = ADX(inputs, timeperiod=14)
  ## count
  # if adx[-1] > adx_stand:
  #   count_buy += 1
  #   results['Type'].append('Buy')
  # elif adx[-1] == adx_stand:
  #   count_neutural +=1
  #   results['Type'].append('neutural')
  # else:
  #   count_sell+=1
  #   results['Type'].append('Sell')
  results['Number'].append(to_str(round(adx[-1], 6)))
  results['Type'].append('-')

  ##### Calculate William%R(14) and print to console    --> DONE    #####
  wr = WILLR(inputs, timeperiod=14)
  ## count
  if numpy.isnan(wr[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if wr[-1] > wr_stand and wr[-1] <-20:
      count_buy += 1
      if wr[-1] > -40:
        results['Type'].append('Strong Buy')
      else:
        results['Type'].append('Buy')
    elif wr[-1] >-20:
      count_neutural +=1
      results['Type'].append('OverBought')
    elif wr[-1] <=-45 and wr[-1]>=-55 :
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      if wr[-1]<-60 and wr[-1]>-80:
        results['Type'].append('Strong Sell')
      elif wr[-1]<-80:
        results['Type'].append('Over Sell')
        count_over_sell+=1
      else:
        results['Type'].append('Sell')
  results['Number'].append(to_str(round(wr[-1],6)))
  #### Calculate CCI(14) and print to console    --> IN PROFRESS    #####
  cci = CCI(inputs, timeperiod=14)
  if numpy.isnan(cci[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if cci[-1] > cci_stand and cci[-1] < 200:
      count_buy += 1
      if cci[-1] >100:
        results['Type'].append('Strong Buy')
      else:
        results['Type'].append('Buy')
    elif cci[-1]>200:
        count_neutural +=1
        results['Type'].append('Overbought')
    elif cci[-1] == cci_stand:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      if cci[-1] <-100 and cci[-1] >-200:
        results['Type'].append('Strong Sell')
      elif cci[-1] <-200:
        results['Type'].append('OverSell')
        count_over_sell+=1
      else:
        results['Type'].append('Sell')
  results['Number'].append(to_str(round(cci[-1], 6)))

  # ##### Calculate ATR(14) and print to console    --> IN PROFRESS    #####
  atr = ATR(inputs, timeperiod=14)
  if numpy.isnan(atr[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if atr[-1] > atr_stand:
      results['Type'].append('More Volatility')
    else:
      results['Type'].append('Less Volatility')
  results['Number'].append(to_str(round(atr[-1], 6)))
  #### Calculate HIGHS/LOWS(14) and print to console     --> IN PROGRESS    #####
  results['Number'].append("-")
  results['Type'].append('-')
  # ##### Calculate U Oscilator(14) and print to console    --> DONE    #####
  uo = ULTOSC(inputs, timeperiod1=7, timeperiod2=14, timeperiod3=28)
  ## count
  if numpy.isnan(uo[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if uo[-1] > 50 and uo[-1] < 70:
      count_buy += 1
      if uo[-1] >60:
        results['Type'].append('Strong Buy')
      else:
        results['Type'].append('Buy')
    elif uo[-1]>70:
        count_neutural +=1
        results['Type'].append('Overbought')
    elif uo[-1] == 50:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      if uo[-1] <40 and uo[-1] >30:
        results['Type'].append('Strong Sell')
      elif uo[-1] <30:
        results['Type'].append('OverSell')
        count_over_sell+=1
      else:
        results['Type'].append('Sell')
  results['Number'].append(to_str(round(uo[-1], 6)))
  # results['Type'].append('-')
  # ##### Calculate ROC(9) and print to console    --> DONE    #####
  roc = ROC(inputs, timeperiod=9)
  if numpy.isnan(roc[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if roc[-1] > roc_stand:
      count_buy += 1
      results['Type'].append('Buy')
    elif roc[-1] == roc_stand:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      results['Type'].append('Sell')
  results['Number'].append(to_str(round(roc[-1], 6)))
  # results['Type'].append('-')
  # #### Calculate SMA(5) and print to console    --> DONE    #####
  sma5 = SMA(inputs, timeperiod=5)
  if numpy.isnan(sma5[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if sma5[-1] < sma5_stand:
      count_buy += 1
      results['Type'].append('Buy')
    elif sma5[-1] == sma5_stand:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      results['Type'].append('Sell')
  results['Number'].append(to_str(round(sma5[-1], 6)))
  # results['Type'].append('-')
  # #### Calculate SMA(10) and print to console    --> DONE    #####
  sma10 = SMA(inputs, timeperiod=10)
  if numpy.isnan(sma10[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if sma10[-1] < sma10_stand:
      count_buy += 1
      results['Type'].append('Buy')
    elif sma10[-1] == sma10_stand:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      results['Type'].append('Sell')
  results['Number'].append(to_str(round(sma10[-1], 6)))
  # results['Type'].append('-')
  # #### Calculate SMA(20) and print to console    --> DONE    #####
  sma20 = SMA(inputs, timeperiod=20)
  if numpy.isnan(sma20[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if sma20[-1] < sma20_stand:
      count_buy += 1
      results['Type'].append('Buy')
    elif sma20[-1] == sma20_stand:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      results['Type'].append('Sell')
  results['Number'].append(to_str(round(sma20[-1], 6)))
  # results['Type'].append('-')
  # #### Calculate SMA(50) and print to console    --> DONE    #####
  sma50 = SMA(inputs, timeperiod=50)
  if numpy.isnan(sma50[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if sma50[-1] < sma50_stand:
      count_buy += 1
      results['Type'].append('Buy')
    elif sma50[-1] == sma50_stand:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      results['Type'].append('Sell')
  results['Number'].append(to_str(round(sma50[-1], 6)))
  # results['Type'].append('-')
  # #### Calculate SMA(100) and print to console    --> DONE    #####
  sma100 = SMA(inputs, timeperiod=100)
  if numpy.isnan(sma100[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if sma100[-1] < sma100_stand:
      count_buy += 1
      results['Type'].append('Buy')
    elif sma100[-1] == sma100_stand:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      results['Type'].append('Sell')
  results['Number'].append(to_str(round(sma100[-1], 6)))
  # results['Type'].append('-')
  # #### Calculate SMA(200) and print to console    --> DONE    #####
  sma200 = SMA(inputs, timeperiod=200)
  if numpy.isnan(sma200[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if sma200[-1] < sma200_stand:
      count_buy += 1
      results['Type'].append('Buy')
    elif sma200[-1] == sma200_stand:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      results['Type'].append('Sell')
  results['Number'].append(to_str(round(sma200[-1], 6)))
  # results['Type'].append('-')
  # ##### Calculate EMA(5) and print to console    --> DONE    #####
  ema5 = EMA(inputs, timeperiod=5)
  if numpy.isnan(ema5[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if ema5[-1] < ema5_stand:
      count_buy += 1
      results['Type'].append('Buy')
    elif ema5[-1] == ema5_stand:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      results['Type'].append('Sell')
  results['Number'].append(to_str(round(ema5[-1], 6)))
  # results['Type'].append('-')
  # ##### Calculate EMA(10) and print to console    --> DONE    #####
  ema10 = EMA(inputs, timeperiod=10)
  if numpy.isnan(ema10[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if ema10[-1] < ema10_stand:
      count_buy += 1
      results['Type'].append('Buy')
    elif ema10[-1] == ema10_stand:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      results['Type'].append('Sell')
  results['Number'].append(to_str(round(ema10[-1], 6)))
  # results['Type'].append('-')
  # ##### Calculate EMA(20) and print to console    --> DONE    #####
  ema20 = EMA(inputs, timeperiod=20)
  if numpy.isnan(ema20[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if ema20[-1] < ema20_stand:
      count_buy += 1
      results['Type'].append('Buy')
    elif ema20[-1] == ema20_stand:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      results['Type'].append('Sell')
  results['Number'].append(to_str(round(ema20[-1], 6)))
  # results['Type'].append('-')
  # #### Calculate EMA(50) and print to console    --> DONE    #####
  ema50 = EMA(inputs, timeperiod=50)
  if numpy.isnan(ema50[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if ema50[-1] < ema50_stand:
      count_buy += 1
      results['Type'].append('Buy')
    elif ema50[-1] == ema50_stand:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      results['Type'].append('Sell')
  results['Number'].append(to_str(round(ema50[-1], 6)))
  # results['Type'].append('-')
  # #### Calculate EMA(100) and print to console    --> DONE    #####
  ema100 = EMA(inputs, timeperiod=100)
  if numpy.isnan(ema100[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if ema100[-1] < ema100_stand:
      count_buy += 1
      results['Type'].append('Buy')
    elif ema100[-1] == ema100_stand:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      results['Type'].append('Sell')
  results['Number'].append(to_str(round(sma100[-1], 6)))
  # results['Type'].append('-')
  # #### Calculate EMA(200) and print to console    --> DONE    #####
  ema200 = EMA(inputs, timeperiod=200)
  if numpy.isnan(ema200[-1]):
    count_neutural +=1
    results['Type'].append('-')
  else:
    if ema200[-1] < ema200_stand:
      count_buy += 1
      results['Type'].append('Buy')
    elif ema200[-1] == ema200_stand:
      count_neutural +=1
      results['Type'].append('neutural')
    else:
      count_sell+=1
      results['Type'].append('Sell')

  results['Number'].append(to_str(round(ema200[-1], 6)))
  # results['Type'].append('-')
  results['Number'].append(to_str(count_buy))
  results['Type'].append('Buy')
  results['Number'].append(to_str(count_sell))
  results['Type'].append('Sell')
  results['Number'].append(to_str(count_neutural))
  results['Type'].append('neutural')
  results['Number'].append(to_str(count_over_sell))
  results['Type'].append('Over Sell')
  # print(len(results['Type']),len(results['Number']))
  return results
def getData(symbol,interval, market):
    #reset
    arr_close =[]
    arr_high=[]
    arr_low =[]
    arr_open =[]
    arr_volume =[]
    headers = {
              "Accept": "application/json",
          }
    fuck=None
    if market =="binance":
      url = 'https://api.binance.com/api/v1/klines'
      params = {
        'symbol':symbol.upper(),
        'interval':interval
      }
      response = requests.get(url=url,params=params,headers=headers)
      fuck= response.json()
    else:
      url = 'https://api.cryptowat.ch/markets/'+market+'/'+symbol+'/ohlc'
      params = {
        'periods':getInteval(interval),
      }
      response = requests.get(url=url,params=params,headers=headers)
      fuck= response.json()
      fuck = fuck["result"][str(getInteval(interval))]
    i=0
    while i < len(fuck):
        arr_open.append(float(fuck[i][1]))
        arr_high.append(float(fuck[i][2]))
        arr_low.append(float(fuck[i][3]))
        arr_close.append(float(fuck[i][4]))
        arr_volume.append(float(fuck[i][5]))
        i+=1
    inputs = {
      'open':  numpy.array(arr_open),
      'high': numpy.array(arr_high),
      'low':  numpy.array(arr_low),
      'close': numpy.array(arr_close),
      'volume':  numpy.array(arr_volume)
    }
    return inputs
if __name__ == '__main__':
    inputs = getData("manaeth","1h","bittrex")
    results = calculate(inputs)
    print(results)