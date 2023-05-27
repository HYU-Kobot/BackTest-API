#pip install xgboost
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# 데이터셋 로드
df = pd.read_csv("crypto_data.csv")

# 종가(close) 정보 추출
df = df[['time', 'Close']]
df = df.set_index('time')

# 스케일링
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))
df = scaler.fit_transform(df)

# 시계열 데이터셋 생성
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)

look_back = 100
X, Y = create_dataset(df, look_back)

# 훈련 데이터와 검증 데이터로 분리
X_train, X_valid, y_train, y_valid = train_test_split(X, Y, test_size=0.2, train_size = 0.8,shuffle=True)
print(y_valid)
print(X_train.size)
# XGBoost 모델 학습
dtrain = xgb.DMatrix(X_train, label=y_train)
dvalid = xgb.DMatrix(X_valid, label=y_valid)
params = {'objective': 'reg:squarederror', 'max_depth': 4, 'learning_rate': 0.1}
num_rounds = 200
model = xgb.train(params, dtrain, num_rounds, evals=[(dvalid, 'valid')], early_stopping_rounds=10)

# 검증 데이터 예측
valid_pred = model.predict(dvalid)

# 검증 데이터의 평균 제곱근 오차(RMSE) 계산
valid_rmse = np.sqrt(mean_squared_error(y_valid, valid_pred))
print(f"Validation RMSE: {valid_rmse}")

# 테스트 데이터 예측
test_start = X_valid[-1].reshape(1, -1)
test_pred = []
for i in range(30):
    test_input = test_start.reshape(1, look_back)
    test_output = model.predict(xgb.DMatrix(test_input))
    test_pred.append(test_output[0])
    test_start = np.append(test_start[:, 1:], test_output).reshape(1, -1)

# 테스트 데이터 예측 결과 시각화
import matplotlib.pyplot as plt

day_new = np.arange(1, 61)
day_pred = np.arange(61, 101)

plt.plot(day_new, scaler.inverse_transform(y_valid[-100:].reshape(-1,1)))
#plt.plot(day_pred, scaler.inverse_transform(test_pred).reshape(-1,1))
plt.show()


'''
# train1
lgbm = LGBMClassifier(n_estimators = 400, learning_rate = 0.3, max_depth = 3)
lgbm.fit(X_train, y_train)
'''
'''
# prediction
w_pred = lgbm.predict(X_test)
w_pred_proba = lgbm.predict_proba(X_test)[:,1]

# confusion matrix
get_clf_eval(y_test, w_pred, w_pred_proba)

# importance plot
fig, ax = plt.subplots(figsize = (10,12))
plot_importance(lgbm, ax=ax)
'''

'''
# 종가(close) 정보 추출
df = df[['time', 'Close']]
df = df.set_index('time')
print(df)
# 스케일링
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))
df = scaler.fit_transform(df)

# 시계열 데이터셋 생성
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        a = dataset[i:(i+look_back), 0]
        dataX.append(a)
        dataY.append(dataset[i + look_back, 0])
    return np.array(dataX), np.array(dataY)

look_back = 100
X, Y = create_dataset(df, look_back)
# 데이터 가


print(datetime.timedelta(days=5))
print(datetime.datetime.now())
time_now = datetime.datetime.now() + datetime.timedelta(days=5)
time_now = time_now.strftime("%Y%m%d")

Train = df[df['date'] <= time_now]
Test = df[df['date'] > time_now]

Train.reset_index(drop=True, inplace=True)
Test.reset_index(drop=True, inplace=True)

cols = df.columns.tolist()
cols.remove('target')

X_train, X_valid, y_train, y_valid = train_test_split(Train[cols], Train['target'], test_size=0.2, train_size = 0.8,random_state=13)
'''



'''
version 20230509
# Train+Valid/Test 데이터 분할
time_now = datetime.datetime(2022,12,1,9,0,0,0)

Train = df[df['date_time_kst'] <= time_now]
Test = df[df['date_time_kst'] > time_now]
Test = Test[:-1] # 마지막 데이터는 next_trade_price가 NaN이므로 제외

#<iteration=100>번동안 Train/Valid/Test 수행
val_err = 0
test_err = 0
iteration = 100

for i in range(iteration):
    # Train/Valid 데이터 분할
    train, valid = train_test_split(Train,train_size=0.8,random_state=1010+i)
    X_train, X_valid, y_train, y_valid = train_test_split(train[cols], train['next_trade_price'], test_size=0.2, train_size = 0.8,random_state=i)

    train_ds = lgb.Dataset(X_train,label=y_train)
    val_ds = lgb.Dataset(X_valid,label=y_valid)

    params = {
        'learning_rate': 0.05,
        'boosting_type': 'gbdt',
        'objective': 'tweedie',
        'tweedie_variance_power': 1.1,
        'metric': 'mae',
        'sub_row': 0.75,
        'lambda_l2': 0.1,
        'force_col_wise': True 
    }

    model_t = lgb.train(params,
                        train_ds,
                        2000
                        ,val_ds,
                        verbose_eval = 100,
                        early_stopping_rounds=100
                        )



    # Validation
    y_pred = model_t.predict(valid[cols])
    val_err += mean_absolute_percentage_error(valid['next_trade_price'],y_pred)

    # Test
    X_test = Test[cols]
    y_test = Test['next_trade_price']

    y_pred_test = model_t.predict(X_test)
    test_err += mean_absolute_percentage_error(y_test,y_pred_test)

print('Trade price validation....Mean absolute error is\n',val_err/iteration*100,"%")
print('Trade price prediction....Mean absolute error is\n',test_err/iteration*100,"%")
'''

'''
version 20230526

#pip install xgboost
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
import datetime
from datetime import timedelta
import lightgbm as lgb

# 학습중 warning 출력 제거
import warnings
warnings.filterwarnings('ignore')

# 데이터셋 로드
df = pd.read_csv("kobot_candle_data.csv")
df['date_time_kst'] = pd.to_datetime(df['date_time_kst'])
df = df.sort_values(by='date_time_kst')
df.reset_index(drop=True)
df['next_trade_price'] = df['trade_price'].shift(-1)

#rsi(period=14) 구하기
period = 14
delta = df['trade_price'].diff().dropna()
gains = delta.where(delta > 0, 0)
losses = -delta.where(delta < 0, 0)

avg_gain = gains.rolling(window=period).mean()
avg_loss = losses.rolling(window=period).mean()
rs = avg_gain/avg_loss
rsi = 100 - (100 / (1+rs))

df['rsi'] = df.index.map(rsi)

#macd 구하기
k = df['trade_price'].ewm(span=12, adjust=False, min_periods=12).mean()
d = df['trade_price'].ewm(span=26, adjust=False, min_periods=26).mean()
macd = k - d
signal = macd.ewm(span=9, adjust=False, min_periods=9).mean()
oscilator = macd - signal
df['macd'] = df.index.map(macd)
df['signal'] = df.index.map(signal)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# 머신러닝 parameter (입력받기 : 수수료비율(%), 손절비율(%), 예측기간, 예측기간 내 기대상승률(매수조건에 사용))
charge = 0.2
stop_loss = 2 # 투자금 대비 2 % 하락
forecast_days = 1
expected_rise = 0.3 # 0.3% 상승


# Train column 정리
#cols = ['trade_price','rsi','macd','next_trade_price'] # or ['opening_price','high_price','low_price','trade_price','rsi','macd','signal','next_trade_price']
cols = df.columns.tolist()
cols.remove('id')
cols.remove('acc_trade_price')
cols.remove('acc_trade_volume')
cols.remove('date_time_kst')
cols.remove('exchange')
cols.remove('market')
cols.remove('time_unit')
'''
pred_cols = cols
pred_cols.remove('high_price')
pred_cols.remove('low_price')
pred_cols.remove('opening_price')
pred_cols.remove('trade_price')
'''

# Train+Valid/Test 데이터 분할
time_now = datetime.datetime(2022,1,1,9,0,0,0)
time_max = datetime.datetime(2022,1,31,9,0,0,0)

position = 0
asset = 10000
buy_price = 0
asset_when_bought = 0

res_df = pd.DataFrame(data={'timestamp': [], 'prev' : [], 'real': [], 'pred': [], 'diff': [], 'position': [], 'asset': []})


while time_now <= time_max:

    Train = df[df['date_time_kst'] < time_now - datetime.timedelta(days=1)]
    Test = df[df['date_time_kst'] >= time_now - datetime.timedelta(days=1)].head(forecast_days)

    #print("Test\n",Test)
    #print("Train tail \n",Train.iloc[-1])
    #print("Test head \n", Test.iloc[0])

    #손절 고려하여 balance update
    prev2_trade_price = Train.iloc[-1]['trade_price']
    prev_trade_price = Test.iloc[0]['trade_price']
    prev_low_price = Test.iloc[0]['low_price']
    #print("prev2 trade price, prev trade price, prev low price\n",prev2_trade_price, prev_trade_price, prev_low_price)
    
    if position == 1:
        #print("prev_low_price : ",prev_low_price, "buy_price : ",buy_price)
        if prev_low_price < buy_price * (1-stop_loss/100):
            asset = asset_when_bought * (1-stop_loss/100)
        else:
            asset += asset * ((prev_trade_price-prev2_trade_price)/prev2_trade_price)


    #<iteration>번동안 Train/Valid/Test 수행
    val_err = 0
    test_err = 0
    iteration = 1

    real = 0
    pred = 0
    for i in range(iteration):

        # Train/Valid 데이터 분할
        train, valid = train_test_split(Train,train_size=0.8,random_state=i)
        X_train, X_valid, y_train, y_valid = train_test_split(train[cols], train['next_trade_price'], test_size=0.2, train_size = 0.8,random_state=i)

        train_ds = lgb.Dataset(X_train,label=y_train)
        val_ds = lgb.Dataset(X_valid,label=y_valid)

        params = {
            'learning_rate': 0.05,
            'boosting_type': 'gbdt',
            'objective': 'tweedie',
            'tweedie_variance_power': 1.1,
            'metric': 'mae',
            'sub_row': 0.75,
            'lambda_l2': 0.1,
            'force_col_wise': True 
        }

        model_t = lgb.train(params,
                            train_ds,
                            2000
                            ,val_ds,
                            verbose_eval = 100,
                            early_stopping_rounds=100
                            )



        # Validation
        y_pred = model_t.predict(valid[cols])
        val_err += mean_absolute_percentage_error(valid['next_trade_price'],y_pred)

        # Test
        X_test = Test[cols]
        y_test = Test['next_trade_price']

        y_pred_test = model_t.predict(X_test)
        test_err += mean_absolute_percentage_error(y_test,y_pred_test)


        real = Test.iloc[-1]['next_trade_price']
        prev = prev_trade_price
        pred += y_pred_test[0]

    pred /= iteration

    # 매수매도여부판단
    # ...
    if (pred-prev)/prev*100 >= expected_rise:
        if position == 0:
            buy_price = prev
            asset_when_bought = asset
        position = 1
    else:
        position = 0

    res_df = res_df.append({'timestamp': time_now, 
                            'prev': prev, 
                            'real': real, 
                            'pred': pred, 
                            'diff': (real-pred)/real*100, 
                            'position' : position, 
                            'asset' : asset
                            }, 
                            ignore_index=True)
        
    print('Trade price validation....Mean absolute error is\n',val_err/iteration*100,"%")
    print('Trade price prediction....Mean absolute error is\n',test_err/iteration*100,"%")

    time_now += datetime.timedelta(days=1)

print(res_df)
res_df.to_csv('res_df.csv', index=False)
'''