import numpy
from talib.abstract import *
import requests
import json

def to_str(var):
    return str(list(numpy.reshape(numpy.asarray(var), (1, numpy.size(var)))[0]))[1:-1]

def getData(symbol,interval):
    #reset
    count_buy = 0
    count_sell = 0
    count_neutural = 0

    url = 'https://api.binance.com/api/v1/klines'
    headers = {
            "Accept": "application/json",
        }
    params = {
      'symbol':symbol.upper(),
      'interval':interval
    }
    response = requests.get(url=url,params=params,headers=headers)
    fuck= response.json()
    i=0;
    arr_close =[]
    arr_high=[]
    arr_low =[]
    arr_open =[]
    arr_volume =[]
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
    rsi_stand=10
    sma10_stand=10
    adx_stand=10
    wr_stand=10
    uo_stand=10
    roc_stand=10
    ema5_stand=10
    ema10_stand=10
    ema20_stand=10
    ema50_stand=10
    ema100_stand=10
    ema200_stand=10
    sma5_stand=10
    sma10_stand=10
    sma20_stand=10
    sma50_stand=10
    sma100_stand=10
    sma200_stand=10
    atr_stand=10
    cci_stand=10
    results=''
    #####   Calculate RSI(14) and print to console    --> DONE    #####  
    # print ("########    RSI(14)    ##########")
    results+="1. RSI(14) = "
    real = RSI(inputs, timeperiod=14)
    ## count
    if real[-1] > rsi_stand:
      count_buy += 1
      results+=to_str(real[-1])+ " --> RSI(14) > " + str(rsi_stand) + " --> buy " + "\n"
    elif real[-1] == rsi_stand:
      count_neutural +=1
      results+=to_str(real[-1])+ " --> RSI(14) = " +  str(rsi_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(real[-1])+ " --> RSI(14) < " +  str(rsi_stand) + " --> sell " + "\n"
    
    #### Calculate STOCH(9,6) and print to console     --> IN PROGRESS    #####
    # print "########    STOCH(9,6)    ##########"
    results+="2. STOCH(9,6) = "
    slowk, slowd = STOCH(inputs,fastk_period=9, slowk_period=6, slowk_matype=0, slowd_period=6, slowd_matype=0)
    # print "########    slowk    ##########"
    results+="######## slowk    ##########      "
    results+=to_str(slowk[-1])+"\n"
    # print   slowk[-1]
    # print "########    slowk    ##########"
    # print   slowd[-1]
    results+="######## slowd    ##########      "
    results+=to_str(slowd[-1])+"\n"

    #### Calculate STOCHRSI(14) and print to console     --> IN PROGRESS    #####
    # print "########    STOCHRSI(14)    ##########"
    results+="3. STOCHRSI(14) = "
    
    #### Calculate MACD(12,26,9) and print to console    --> IN PROGRESS     #####
    # print "########    MACD(12,26,9)    ##########"
    results+="4. MACD(12,26,9) = "
    macd, macdsignal, macdhist = MACD(inputs, fastperiod=12, slowperiod=26, signalperiod=9)
    results+="########    macd    ##########      "
    results+=to_str(macd[-1])+"\n"
    # print "########    macd    ##########"
    # print  macd[-1]
    # print "########    macdsignal    ##########"
    # print  macdsignal[-1]
    results+="########    macdsignal    ##########     "
    results+=to_str(macdsignal[-1])+"\n"
    # print "########    macdhist    ##########"
    # print  macdhist[-1]
    results+="########    macdhist    ##########     "
    results+=to_str(macdhist[-1])+"\n"

   ##### Calculate ADX(14) and print to console    --> DONE    #####
    # print ("########    ADX(14)    ##########")
    results+="3. ADX(14) = "
    adx = ADX(inputs, timeperiod=14)
    adx_type = "ADX(14)"
     ## count
    if adx[-1] > adx_stand:
      count_buy += 1
      results+=to_str(adx[-1])+ " --> "+adx_type+"> " + str(adx_stand) + " --> buy " + "\n"
    elif adx[-1] == sma10_stand:
      count_neutural +=1
      results+=to_str(adx[-1])+ " --> "+adx_type+" = " + str(adx_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(adx[-1])+ " --> "+adx_type+" < " + str(adx_stand) + " --> sell " + "\n"
    
    ##### Calculate William%R(14) and print to console    --> DONE    #####
    # print ("########    William%R(14)    ##########")
    results+="4. William%R(14) = "
    wr = WILLR(inputs, timeperiod=14)
    adx_type = "William%R(14)"
     ## count
    if wr[-1] > wr_stand:
      count_buy += 1
      results+=to_str(wr[-1])+ " --> "+adx_type+"> " + str(wr_stand) + " --> buy " + "\n"
    elif wr[-1] == wr_stand:
      count_neutural +=1
      results+=to_str(wr[-1])+ " --> "+adx_type+" = " + str(wr_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(wr[-1])+ " --> "+adx_type+" < " + str(wr_stand) + " --> sell " + "\n"
    # print(wr[-1])  
    #### Calculate CCI(14) and print to console    --> IN PROFRESS    #####
    # print "########    CCI(14)    ##########"
    results+="7. CCI(14) = "
    cci = CCI(inputs, timeperiod=14)
    if cci[-1] > cci_stand:
      count_buy += 1
      results+=to_str(cci[-1])+ " --> ATR(14) > " +  str(cci_stand) + " --> buy " + "\n"
    elif cci[-1] == cci_stand:
      count_neutural +=1
      results+=to_str(cci[-1])+ " --> ATR(14) = " +  str(cci_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(cci[-1])+ " --> ATR(14) < " + str(cci_stand) + " --> sell " + "\n"
    # print  cci[-1]

    # ##### Calculate ATR(14) and print to console    --> IN PROFRESS    #####
    # print "########    ATR(14)    ##########"
    results+="8. ATR(14) = "
    atr = ATR(inputs, timeperiod=14)
    if atr[-1] > atr_stand:
      count_buy += 1
      results+=to_str(atr[-1])+ " --> ATR(14) > " + str(atr_stand) + " --> buy " + "\n"
    elif atr[-1] == atr_stand:
      count_neutural +=1
      results+=to_str(atr[-1])+ " --> ATR(14) = " + str(atr_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(atr[-1])+ " --> ATR(14) < " + str(atr_stand) + " --> sell " + "\n"
    # print  atr[-1]

    #### Calculate HIGHS/LOWS(14) and print to console     --> IN PROGRESS    #####
    # print "########    HIGHS/LOWS(14)    ##########"
    results+="9. HIGHS/LOWS(14) = "

    # ##### Calculate U Oscilator(14) and print to console    --> DONE    #####
    # print ("########    U Oscilator(7,14,28)    ##########")
    results+="5. U Oscilator(7,14,28) = "
    uo = ULTOSC(inputs, timeperiod1=7, timeperiod2=14, timeperiod3=28)
    adx_type = "U Oscilator(7,14,28)"
     ## count
    if uo[-1] > wr_stand:
      count_buy += 1
      results+=to_str(uo[-1])+ " --> "+adx_type+"> " + str(uo_stand) + " --> buy " + "\n"
    elif uo[-1] == wr_stand:
      count_neutural +=1
      results+=to_str(uo[-1])+ " --> "+adx_type+" = " + str(uo_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(uo[-1])+ " --> "+adx_type+" < " + str(uo_stand) + " --> sell " + "\n"
    
    # ##### Calculate ROC(9) and print to console    --> DONE    #####
    # print "########    ROC(9)    ##########"
    results+="11. ROC(9) = "
    roc = ROC(inputs, timeperiod=9)
    if roc[-1] > roc_stand:
      count_buy += 1
      results+=to_str(roc[-1])+ " --> ROC(9) > " +  str(roc_stand) + " --> buy " + "\n"
    elif roc[-1] == roc_stand:
      count_neutural +=1
      results+=to_str(roc[-1])+ " --> ROC(9) = " +  str(roc_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(roc[-1])+ " --> ROC(9) < " + str(roc_stand) + " --> sell " + "\n"
    # print  roc[-1]

    # #### Calculate SMA(5) and print to console    --> DONE    #####
    # print "########    SMA(5)    ##########"
    results+="12. SMA(5) = "
    sma5 = SMA(inputs, timeperiod=5)
    if sma5[-1] > sma5_stand:
      count_buy += 1
      results+=to_str(sma5[-1])+ " --> SMA(5) > " + str(sma5_stand) + " --> buy " + "\n"
    elif sma5[-1] == sma5_stand:
      count_neutural +=1
      results+=to_str(sma5[-1])+ " --> SMA(5) = " + str(sma5_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(sma5[-1])+ " --> SMA(5) < " + str(sma5_stand) + " --> sell " + "\n"
    # print  sma5[-1]

    # #### Calculate SMA(10) and print to console    --> DONE    #####
    # print "########    SMA(10)    ##########"
    results+="13. SMA(10) = "
    sma10 = SMA(inputs, timeperiod=10)
    if sma10[-1] > sma10_stand:
      count_buy += 1
      results+=to_str(sma10[-1])+ " --> SMA(10) > " + str(sma10_stand) + " --> buy " + "\n"
    elif sma10[-1] == sma10_stand:
      count_neutural +=1
      results+=to_str(sma10[-1])+ " --> SMA(10) = " + str(sma10_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(sma10[-1])+ " --> SMA(10) < " + str(sma10_stand) + " --> sell " + "\n"
    # print  sma10[-1]

    # #### Calculate SMA(20) and print to console    --> DONE    #####
    # print "########    SMA(20)    ##########"
    results+="14. SMA(20) = "
    sma20 = SMA(inputs, timeperiod=20)
    if sma20[-1] > sma20_stand:
      count_buy += 1
      results+=to_str(sma20[-1])+ " --> SMA(20) > " + str(sma20_stand) + " --> buy " + "\n"
    elif sma20[-1] == sma20_stand:
      count_neutural +=1
      results+=to_str(sma20[-1])+ " --> SMA(20) = " + str(sma20_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(sma20[-1])+ " --> SMA(20) < " + str(sma20_stand) + " --> sell " + "\n"
    # print  sma20[-1]

    # #### Calculate SMA(50) and print to console    --> DONE    #####
    # print "########    SMA(50)    ##########"
    results+="15. SMA(50) = "
    sma50 = SMA(inputs, timeperiod=50)
    if sma50[-1] > sma50_stand:
      count_buy += 1
      results+=to_str(sma50[-1])+ " --> SMA(50) > " + str(sma50_stand) + " --> buy " + "\n"
    elif sma50[-1] == sma50_stand:
      count_neutural +=1
      results+=to_str(sma50[-1])+ " --> SMA(50) = " + str(sma50_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(sma50[-1])+ " --> SMA(50) < " + str(sma50_stand) + " --> sell " + "\n"
    # print  sma50[-1]
    
    # #### Calculate SMA(100) and print to console    --> DONE    #####
    # print "########    SMA(100)    ##########"
    results+="16. SMA(100) = "
    sma100 = SMA(inputs, timeperiod=100)
    if sma100[-1] > sma100_stand:
      count_buy += 1
      results+=to_str(sma100[-1])+ " --> SMA(100) > " + str(sma100_stand) + " --> buy " + "\n"
    elif sma100[-1] == sma100_stand:
      count_neutural +=1
      results+=to_str(sma100[-1])+ " --> SMA(100) = " + str(sma100_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(sma100[-1])+ " --> SMA(100) < " + str(sma100_stand) + " --> sell " + "\n"
    # print  sma100[-1]

    # #### Calculate SMA(200) and print to console    --> DONE    #####
    # print "########    SMA(200)    ##########"
    results+="17. SMA(200) = "
    sma200 = SMA(inputs, timeperiod=200)
    if sma200[-1] > sma200_stand:
      count_buy += 1
      results+=to_str(sma200[-1])+ " --> SMA(200) > " + str(sma200_stand) + " --> buy " + "\n"
    elif sma200[-1] == sma200_stand:
      count_neutural +=1
      results+=to_str(sma200[-1])+ " --> SMA(200) = " + str(sma200_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(sma200[-1])+ " --> SMA(200) < " + str(sma200_stand) + " --> sell " + "\n"
    # print  sma200[-1]

    # ##### Calculate EMA(5) and print to console    --> DONE    #####
    # print "########    EMA(5)    ##########"
    results+="18. EMA(5) = "
    ema5 = EMA(inputs, timeperiod=5)
    if ema5[-1] > ema5_stand:
      count_buy += 1
      results+=to_str(ema5[-1])+ " --> EMA(5) > " + str(ema5_stand) + " --> buy " + "\n"
    elif ema5[-1] == ema5_stand:
      count_neutural +=1
      results+=to_str(ema5[-1])+ " --> EMA(5) = " + str(ema5_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(ema5[-1])+ " --> EMA(5) < " + str(ema5_stand) + " --> sell " + "\n"
    # print  ema5[-1]

    # ##### Calculate EMA(10) and print to console    --> DONE    #####
    # print "########    EMA(10)    ##########"
    results+="19. EMA(10) = "
    ema10 = EMA(inputs, timeperiod=10)
    if ema10[-1] > ema10_stand:
      count_buy += 1
      results+=to_str(ema10[-1])+ " --> EMA(10) > " + str(ema10_stand) + " --> buy " + "\n"
    elif ema10[-1] == ema10_stand:
      count_neutural +=1
      results+=to_str(ema10[-1])+ " --> EMA(10) = " + str(ema10_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(ema10[-1])+ " --> EMA(10) < " + str(ema10_stand) + " --> sell " + "\n"
    # print  ema10[-1]

    # ##### Calculate EMA(20) and print to console    --> DONE    #####
    # print "########    EMA(20)    ##########"
    results+="20. EMA(20) = "
    ema20 = EMA(inputs, timeperiod=20)
    # print  ema20[-1]
    if ema20[-1] > ema20_stand:
      count_buy += 1
      results+=to_str(ema20[-1])+ " --> EMA(20) > " + str(ema20_stand) + " --> buy " + "\n"
    elif ema20[-1] == ema20_stand:
      count_neutural +=1
      results+=to_str(ema20[-1])+ " --> EMA(20) = " + str(ema20_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(ema20[-1])+ " --> EMA(20) < " + str(ema20_stand) + " --> sell " + "\n"

    # #### Calculate EMA(50) and print to console    --> DONE    #####
    # print "########    EMA(50)    ##########"
    results+="21. EMA(50) = "
    ema50 = EMA(inputs, timeperiod=50)
    if ema50[-1] > ema50_stand:
      count_buy += 1
      results+=to_str(ema50[-1])+ " --> EMA(50) > " + str(ema50_stand) + " --> buy " + "\n"
    elif ema50[-1] == ema50_stand:
      count_neutural +=1
      results+=to_str(ema50[-1])+ " --> EMA(50) = " + str(ema50_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(ema50[-1])+ " --> EMA(50) < " + str(ema50_stand) + " --> sell " + "\n"
    # print  ema50[-1]

    # #### Calculate EMA(100) and print to console    --> DONE    #####
    # print "########    EMA(100)    ##########"
    results+="22. EMA(100) = "
    ema100 = EMA(inputs, timeperiod=100)
    if ema100[-1] > ema100_stand:
      count_buy += 1
      results+=to_str(ema100[-1])+ " --> EMA(100) > " + str(ema100_stand) + " --> buy " + "\n"
    elif ema100[-1] == ema100_stand:
      count_neutural +=1
      results+=to_str(ema100[-1])+ " --> EMA(100) = " + str(ema100_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(ema100[-1])+ " --> EMA(100) < " + str(ema100_stand) + " --> sell " + "\n"
    # print  ema100[-1]

    # #### Calculate EMA(200) and print to console    --> DONE    #####
    # print "########    EMA(200)    ##########"
    results+="23. EMA(200) = "
    ema200 = EMA(inputs, timeperiod=200)
    if ema200[-1] > ema200_stand:
      count_buy += 1
      results+=to_str(ema200[-1])+ " --> EMA(200) > " +  str(ema200_stand) + " --> buy " + "\n"
    elif ema200[-1] == ema200_stand:
      count_neutural +=1
      results+=to_str(ema200[-1])+ " --> EMA(200) = " +  str(ema200_stand) + " --> neutural " + "\n"
    else:
      count_sell+=1
      results+=to_str(ema200[-1])+ " --> EMA(200) < " + str(ema200_stand) + " --> sell " + "\n"
    # print  ema200[-1]
    results+="total buy signals:"+ str(count_buy) +"\n" +"total sell signal:" +str(count_sell)+"\n"+"total neutural signal:"+"\n"+str(count_neutural)
    return results
