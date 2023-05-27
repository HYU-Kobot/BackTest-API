import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# CSV 파일 로드
res_df = pd.read_csv('res_df.csv')

# 'timestamp'를 datetime 형식으로 변환
res_df['timestamp'] = pd.to_datetime(res_df['timestamp'])

# 데이터 시각화
fig, ax = plt.subplots()
ax.plot(res_df['timestamp'], res_df['diff'], label='diff')
num_points = len(res_df)
ax.xaxis.set_major_locator(mdates.DayLocator(interval=num_points//10))  # x 축 눈금 간격 설정 (1일 간격)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # x 축 눈금 형식 설정 (연-월-일)
plt.xlabel('Date')
plt.ylabel('Difference')
plt.title("Prediction vs Real Difference")
plt.legend()
plt.xticks(rotation=45)  # x 축 눈금 레이블 각도 설정
plt.show()