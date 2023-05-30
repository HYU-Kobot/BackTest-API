import pandas as pd
import quantstats as qs
import matplotlib
import uuid
import math

from kobot.settings import STATICFILES_DIRS
from kobot.settings import BASE_DIR


def backTestKobotAi(res_df, stop_df, market, risk, timeFrame):
    qs.extend_pandas()
    matplotlib.use('agg')

    pd.set_option('display.max_rows', None)

    order_list = []

    merged_df = pd.concat([res_df, stop_df])
    merged_df = merged_df.sort_index()
    merged_df['profit'] = merged_df['asset'].pct_change()

    position = 0

    for index, row in merged_df.iterrows():
        # 코인종류 -> market, 코인갯수 -> amount, 코인갯수에 따른 원화가격, 거래일자 -> tradePrice, 매수인지 매도인지->category
        if position < row['position']:
            order_list.append({'category': 'BUY', 'market': market, 'amount': row['asset']/row['prev'], 'trade_date': index, 'price' : row['prev']})
        elif position > row['position']:
            order_list.append({'category': 'SELL', 'market': market, 'amount': row['asset']/row['prev'], 'trade_date': index, 'price' : row['prev']})
        position = row['position']

    
    for dic in order_list:
        dic['amount'] = math.floor(dic['amount'] * 1000) / 1000
        dic['price'] = math.floor(dic['price'] * 1000) / 1000

    uuidValue = str(uuid.uuid4())
    filename = str(STATICFILES_DIRS)[2:-3] + "/" + uuidValue + ".html"

    qs.reports.html(merged_df['profit'], download_filename=filename, output=filename)
    return [filename, order_list]
