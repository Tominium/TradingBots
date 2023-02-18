from finviz.screener import Screener
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from urllib.request import urlopen
from urllib.request import Request
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import alpaca_trade_api as tradeapi
from time import sleep
from yahoo_fin import stock_info as si
import requests
import re

api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
account = api.get_account()
print(account)

clock = api.get_clock()
if clock.is_open:
    pass
else:
    time_to_open = clock.next_open - clock.timestamp
    sleep(time_to_open.total_seconds())

def get_stock():
    res = requests.get("https://finance.yahoo.com/screener/unsaved/8ebb0ea5-5693-4f33-83ea-cd5edcc6bf99")
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))[0]
    symbols = df["Symbol"].tolist()
    prices = df["Price (Intraday)"].tolist()
    percentChange = df["% Change"].tolist()
    ticker = df.iloc[0,0]
    print(ticker)

    tweets = []
    twitter = Twitter(language='en')
    for tweets_list in twitter.search('$'+ticker, cached=False, count=3):
        tweets.append(tweets_list.text)
        print(plaintext(tweets_list.text))


    print('----------------------')

    google_news = []
    google_url = 'http://news.google.com/news?q=${}&output=rss'.format(ticker)
    for google_result in Newsfeed().search(google_url)[:3]:
        google_news.append(google_result.title)
        print(plaintext(google_result.title))

    print('----------------------')

    yahoo_news = []
    yahoo_url = 'http://finance.yahoo.com/rss/headline?s={}'.format(ticker)
    for yahoo_result in Newsfeed().search(yahoo_url)[:3]:
        yahoo_news.append(yahoo_result.title)
        print(plaintext(yahoo_result.title))

    print('----------------------')

    print(tweets)
    print(yahoo_news)
    print(google_news)
	news_df = (['tweets': tweets, 'google news': google_news, 'yahoo news': yahoo_news])

    dataframe = pd.DataFrame.from_dict(news_df, orient='index')
    dataframe['tweets'] =  [re.sub(r'@[A-Za-z0-9]+','', str(x)) for x in dataframe['tweets']]
    dataframe['tweets'] =  [re.sub('https?://[A-Za-z0-9./]+','', str(x)) for x in dataframe['tweets']]

    analyzer = SentimentIntensityAnalyzer()
    tweet_mean = TextBlob(str(dataframe['tweets'])).sentiment.polarity
    #tweet_score = dataframe['tweets'].apply(analyzer.polarity_scores).tolist()
    google_score = dataframe['google news'].apply(analyzer.polarity_scores).tolist()
    yahoo_score = dataframe['yahoo news'].apply(analyzer.polarity_scores).tolist()
    print(tweet_score)

    #tw_df = pd.DataFrame(tweet_score)
    g_df = pd.DataFrame(google_score)
    y_df = pd.DataFrame(yahoo_score)

    #tweet_mean = (tw_df['compound'].mean())
    google_mean = (g_df['compound'].mean())
    yahoo_mean = (y_df['compound'].mean())

    combined_mean = tweet_mean + google_mean + yahoo_mean
    mean = round((combined_mean/3), 2)
    print('The mean is {}'.format(mean))

    y = s.get_live_price(ticker)
    print(y)
    current_bal = account.cash
    spending_bal = float(current_bal) - int(50000)
    print('Your Current Balance is {}'.format(current_bal))
    z = (round(float(spending_bal)/(y)))
    lp = float(y)-float(y)*float(0.01)
    tp = float(y)*float(1.01)

    #decide if the sentiment score is positive or Negative
    if mean >= 0.10:
        print("Positive Analysis")
        print('Buying {}'.format(ticker))
        api.submit_order(symbol=ticker,
            qty= z,
            side='buy',
            time_in_force='gtc',
            type='market',
            order_class='bracket',
            stop_loss=dict(stop_price=(lp)),
            take_profit=dict(limit_price=(tp)))


    elif mean <= 0.10:
        print("Negative Analysis")
        print("Shorting {}".format(ticker))
        api.submit_order(symbol=ticker,
            qty=z,
            side='sell',
            time_in_force='gtc',
            type='market',
            order_class='bracket',
            stop_loss=dict(stop_price=float(y)*float(1.01)),
            take_profit=dict(limit_price=(float(y)-float(y)*float(0.01))))

get_stock()

sleep(400)

def check_stocks():
	if len(api.list_positions()) == 0:
		print("none")
		get_stock()
		sleep(400)
		check_stocks()
	while len(api.list_positions()) != 0:
		pass
check_stocks()
