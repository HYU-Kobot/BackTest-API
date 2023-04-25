import pyupbit
import pandas as pd
import quantstats as qs


def BackTestBollingerBand(movingAverage, k, risk):  # 이동평균선, 계수(승수)
    pd.set_option('display.max_rows', None)
    df = pyupbit.get_ohlcv("KRW-BTC")

    df['middle'] = df['close'].rolling(window=movingAverage).mean()
    std = df['close'].rolling(movingAverage).std(ddof=0)
    df['upper'] = df['middle'] + k * std
    df['lower'] = df['middle'] - k * std

    lower_flag = False
    upper_flag = False

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
        if close < lower:
            lower_flag = True
        if lower_flag and (close > lower) and (idx > 0):
            lower_flag = False
            now_coin = SetRiskCoinCount(close, stop_loss, money_balance_list[idx - 1])
            coin_count.append(now_coin + coin_count[idx - 1])
            coin_balance_list.append(now_coin * close + coin_balance_list[idx - 1])
            money_balance_list.append(money_balance_list[idx - 1] - now_coin * close)
            total_balance_list.append(coin_balance_list[idx] + money_balance_list[idx])

            print(index, "coin 개수 : %20.10f " % coin_count[idx], "coin 자산 : %20.10f " % coin_balance_list[idx],
                  "현금자산 : %20.10f " % money_balance_list[idx], "총 자산 : %20.10f " % total_balance_list[idx],
                  "상단 : %20.10f " % upper, "종가 : %20.10f " % close, "하단 : %20.10f " % lower)
            continue

        if (close > upper) and (coin_count[idx - 1] > 0):
            upper_flag = True
        if upper_flag and (close < upper) and (coin_count[idx - 1] > 0) and (idx > 0):
            upper_flag = False
            coin_count.append(0)
            coin_balance_list.append(0)
            money_balance_list.append(coin_count[idx - 1] * close + money_balance_list[idx - 1])
            total_balance_list.append(coin_balance_list[idx] + money_balance_list[idx])

            print(index, "coin 개수 : %20.10f " % coin_count[idx], "coin 자산 : %20.10f " % coin_balance_list[idx],
                  "현금자산 : %20.10f " % money_balance_list[idx], "총 자산 : %20.10f " % total_balance_list[idx],
                  "상단 : %20.10f " % upper, "종가 : %20.10f " % close, "하단 : %20.10f " % lower)
            continue

        if idx > 0:
            money_balance_list.append(money_balance_list[idx - 1])
            coin_count.append(coin_count[idx - 1])
            coin_balance_list.append(coin_count[idx - 1] * close)
            total_balance_list.append(coin_balance_list[idx] + money_balance_list[idx])

        print(index, "coin 개수 : %20.10f " % coin_count[idx], "coin 자산 : %20.10f " % coin_balance_list[idx],
              "현금자산 : %20.10f " % money_balance_list[idx], "총 자산 : %20.10f " % total_balance_list[idx],
              "상단 : %20.10f " % upper, "종가 : %20.10f " % close, "하단 : %20.10f " % lower)

    df['total_balance'] = total_balance_list
    df['profit'] = df['total_balance'].pct_change()

    print(df[['total_balance', 'profit']])

    qs.reports.html(df['profit'], output='./profit.html')
