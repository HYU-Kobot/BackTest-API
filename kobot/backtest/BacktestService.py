from backtest.CandleRepository import findDateAndCloseByMarketAndTimeFrameBetweenStartDateAndEndDate
from .bolidngerband import backTestBollingerBand
from .kobotai import backTestKobotAi
from django.http import JsonResponse 

import os
import pandas as pd

def getBollingerBody(market, startDate, endDate, upperMovingAverage, lowerMovingAverage, upperK, lowerK, riskRate, timeFrame) :
    dic = findDateAndCloseByMarketAndTimeFrameBetweenStartDateAndEndDate("KRW_BTC", "DAY", startDate, endDate)
    df = pd.DataFrame(dic, columns=['Date', 'close'])  
    df = df.set_index('Date') 
    df.index = pd.to_datetime(df.index)

    result = backTestBollingerBand(df, "KRW-BTC", upperMovingAverage, lowerMovingAverage, upperK, lowerK, riskRate, timeFrame)
    fileName = result[0]
    orderList = result[1]
    f = open(fileName)
    content = f.read()
    os.remove(fileName)

    response = JsonResponse({"content" : content, "orderList" : orderList})
    return response

def getKobotAiBody(market, startDate, endDate, riskRate, timeFrame) :
    res_df = pd.read_csv("../ML/res_df.csv")
    res_df = res_df.set_index('timestamp') 
    res_df.index = pd.to_datetime(res_df.index)

    stop_df = pd.read_csv("../ML/stop_df.csv")
    stop_df = stop_df.set_index('timestamp') 
    stop_df.index = pd.to_datetime(stop_df.index)

    result = backTestKobotAi(res_df, stop_df, "KRW_BTC",  riskRate, timeFrame)
    fileName = result[0]
    orderList = result[1]
    f = open(fileName)
    content = f.read()
    os.remove(fileName)

    response = JsonResponse({"content" : content, "orderList" : orderList})
    return response