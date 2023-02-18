from yahoo_fin import stock_info as si
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='Dark2')
import pandas as pd
import requests
from bs4 import BeautifulSoup

res = requests.get("http://finance.yahoo.com/cryptocurrencies")
soup = BeautifulSoup(res.content,'lxml')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))[0]
symbols = df["Symbol"].tolist()
prices = df["Price (Intraday)"].tolist()
percentChange = df["% Change"].tolist()

x = df.iloc[0,0]
x_data = si.get_data(x)
print(x_data)

short_rolling = x_data.rolling(window=20).mean()
print(short_rolling)

long_rolling = x_data.rolling(window=100).mean()
print(long_rolling)


start_date = '2019-01-01'
end_date = '2020-02-01'

fig, ax = plt.subplots(figsize=(16,9))

ax.plot(x_data.loc[start_date:end_date, :].index, x_data.loc[start_date:end_date, 'open'], label='Price')
ax.plot(long_rolling.loc[start_date:end_date, :].index, long_rolling.loc[start_date:end_date, 'open'], label = '100-days SMA')
ax.plot(short_rolling.loc[start_date:end_date, :].index, short_rolling.loc[start_date:end_date, 'open'], label = '20-days SMA')

ax.legend(loc='best')
ax.set_ylabel('Price in $')
my_year_month_fmt = mdates.DateFormatter('%m/%y')
ax.xaxis.set_major_formatter(my_year_month_fmt)


# Using Pandas to calculate a 20-days span EMA. adjust=False specifies that we are interested in the recursive calculation mode.
ema_short = x_data.ewm(span=20, adjust=False).mean()

fig, ax = plt.subplots(figsize=(15,9))

ax.plot(x_data.loc[start_date:end_date, :].index, x_data.loc[start_date:end_date, 'open'], label='Price')
ax.plot(ema_short.loc[start_date:end_date, :].index, ema_short.loc[start_date:end_date, 'open'], label = 'Span 20-days EMA')

ax.legend(loc='best')
ax.set_ylabel('Price in $')
ax.xaxis.set_major_formatter(my_year_month_fmt)
plt.show()
