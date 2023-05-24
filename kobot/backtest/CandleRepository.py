from backtest.models import Candle

def findDateAndCloseByMarketAndTimeFrameBetweenStartDateAndEndDate(market, timeFrame, startDate, endDate):
    dic = { 'Date' : [], 'close' : []}
    Candle.objects.all()
    for c in Candle.objects.raw(
        """
        Select id, trade_price, date_time_kst
            From candle 
            Where market = %s and time_unit= %s
            and date_time_kst between %s and %s
            order by date_time_kst
        """, [market,timeFrame, startDate, endDate]): 
        dic['close'].append(float(c.trade_price))
        dic['Date'].append(c.date_time_kst.strftime("%Y-%m-%d %H:%M:%S"))
    return dic