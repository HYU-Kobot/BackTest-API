from backtest.CandleRepository import findDateAndCloseByMarketAndTimeFrameBetweenStartDateAndEndDate
from .bolidngerband import backTestBollingerBand
from django.http import JsonResponse 

import os
import pandas as pd

def getBody(market, startDate, endDate, upperMovingAverage, lowerMovingAverage, upperK, lowerK, riskRate, timeFrame) :
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