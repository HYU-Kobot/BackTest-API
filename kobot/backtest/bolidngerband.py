import pyupbit
import pandas as pd
import quantstats as qs
import matplotlib
import uuid
import math

from kobot.settings import STATICFILES_DIRS
from kobot.settings import BASE_DIR

def backTestBollingerBand(df, market, upper_moving_average, lower_moving_average, upper_k, lower_k, risk, timeFrame): 
    qs.extend_pandas()
    matplotlib.use('agg')
    
    pd.set_option('display.max_rows', None)
  
    stop_list = []
    order_list = []

    df['upper_middle'] = df['close'].rolling(window=upper_moving_average).mean()
    df['lower_middle'] = df['close'].rolling(window=lower_moving_average).mean()
    upper_std = df['close'].rolling(upper_moving_average).std(ddof=0)
    lower_std = df['close'].rolling(lower_moving_average).std(ddof=0)
    df['upper'] = df['upper_middle'] + upper_k * upper_std
    df['lower'] = df['lower_middle'] - lower_k * lower_std

    lower_flag = False
    upper_flag = False
    loss_flag = False

    first_balance = 10000000000

    coin_count = [0]
    coin_balance_list = [0]
    money_balance_list = [first_balance]
    total_balance_list = [first_balance]

    df['stop_loss_price'] = df['close'] - 1000000

    def SetRiskCoinCount(now_price, stop_loss_price, money_balance):
        count = (money_balance * risk) / (now_price - stop_loss_price)
        return count

    for idx, (close, upper, lower, stop_loss, index) in enumerate(
            zip(df['close'], df['upper'], df['lower'], df['stop_loss_price'], df.index)):

        loss_flag = False
        for loss_dict in stop_list[:]:
            if loss_dict['stop_loss_price'] > close:
                coin_count.append(coin_count[idx - 1] - loss_dict['coin_count'])
                coin_balance_list.append(coin_balance_list[idx - 1] - loss_dict['coin_count'] * close)
                money_balance_list.append(loss_dict['coin_count'] * close + money_balance_list[idx - 1])
                total_balance_list.append(coin_balance_list[idx] + money_balance_list[idx])
                stop_list.remove(loss_dict)
                loss_flag = True
                order_list.append({'category': 'SELL', 'market': market, 'amount': loss_dict['coin_count'], 'tradeDate': index, 'price': close})

        if close < lower:
            lower_flag = True
        if lower_flag and (close > lower) and (idx > 0):
            lower_flag = False
            now_coin = SetRiskCoinCount(close, stop_loss, money_balance_list[idx - 1])
            coin_count.append(now_coin + coin_count[idx - 1])
            coin_balance_list.append(now_coin * close + coin_balance_list[idx - 1])
            money_balance_list.append(money_balance_list[idx - 1] - now_coin * close)
            total_balance_list.append(coin_balance_list[idx] + money_balance_list[idx])
            stop_list.append({'stop_loss_price': stop_loss, 'coin_count': now_coin})
            order_list.append({'category': 'BUY', 'market': market, 'amount': now_coin, 'tradeDate': index, 'price': close})

            # print(index, "coin 개수 : %20.10f " % coin_count[idx], "coin 자산 : %20.10f " % coin_balance_list[idx],
            #       "현금자산 : %20.10f " % money_balance_list[idx], "총 자산 : %20.10f " % total_balance_list[idx],
            #       "상단 : %20.10f " % upper, "종가 : %20.10f " % close, "하단 : %20.10f " % lower)
            continue

        if (close > upper) and (coin_count[idx - 1] > 0):
            upper_flag = True
        if upper_flag and (close < upper) and (coin_count[idx - 1] > 0) and (idx > 0):
            upper_flag = False
            coin_count.append(0)
            coin_balance_list.append(0)
            money_balance_list.append(coin_count[idx - 1] * close + money_balance_list[idx - 1])
            total_balance_list.append(coin_balance_list[idx] + money_balance_list[idx])
            stop_list = []
            order_list.append({'category': 'SELL', 'market': market, 'amount': coin_count[idx-1], 'tradeDate': index, 'price' : close})

            # print(index, "coin 개수 : %20.10f " % coin_count[idx], "coin 자산 : %20.10f " % coin_balance_list[idx],
            #       "현금자산 : %20.10f " % money_balance_list[idx], "총 자산 : %20.10f " % total_balance_list[idx],
            #       "상단 : %20.10f " % upper, "종가 : %20.10f " % close, "하단 : %20.10f " % lower)
            continue

        if idx > 0 and loss_flag == False:
            money_balance_list.append(money_balance_list[idx - 1])
            coin_count.append(coin_count[idx - 1])
            coin_balance_list.append(coin_count[idx - 1] * close)
            total_balance_list.append(coin_balance_list[idx] + money_balance_list[idx])

    #     print(index, "coin 개수 : %20.10f " % coin_count[idx], "coin 자산 : %20.10f " % coin_balance_list[idx],
    #           "현금자산 : %20.10f " % money_balance_list[idx], "총 자산 : %20.10f " % total_balance_list[idx],
    #           "상단 : %20.10f " % upper, "종가 : %20.10f " % close, "하단 : %20.10f " % lower)

    if (len(df.index) != len(total_balance_list)):
        total_balance_list = total_balance_list[0:len(df.index)]
    df['total_balance'] = total_balance_list
    df['profit'] = df['total_balance'].pct_change()
    
    # 코인종류 -> market, 코인갯수 -> amount, 코인갯수에 따른 원화가격, 거래일자 -> tradePrice, 매수인지 매도인지->category
    
    for dic in order_list:
        dic['amount'] = math.floor(dic['amount'] * 1000) / 1000
        dic['price'] = math.floor(dic['price'] * 1000) / 1000
    print(order_list)

    uuidValue = str(uuid.uuid4())
    filename = str(STATICFILES_DIRS)[2:-3] + "/" + uuidValue + ".html"
    
    qs.reports.html(df['profit'], download_filename=filename, output=filename)
    return [filename, order_list]

    # plt.plot(df.index, df['middle'], 'g-', df.index, df['upper'], 'r-', df.index, df['lower'], 'b-', df.index, df['close'],
    #          'k-', df.index, df['stop_loss_price'], 'y-')
    # plt.show()

    



