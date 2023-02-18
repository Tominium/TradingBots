from pattern.web import Twitter, plaintext, Newsfeed
import pandas as pd
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import re
import alpaca_trade_api as tradeapi
from time import sleep
from yahoo_fin import stock_info as s

#authentication and connection details
api_key = 'PKA2Y880SEO2415A8PAI'
api_secret = 'lIS2O0FrsVHLLnMccpebSdgC318UsXNBqH/lC63s'
base_url = 'https://paper-api.alpaca.markets'

#instantiate REST API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
account = api.get_account()
print(account)

#clock = api.get_clock()
#if clock.is_open:
#    pass
#else:
#    time_to_open = clock.next_open - clock.timestamp
#    sleep(time_to_open.total_seconds())

def get_stock():
    res = requests.get("https://finance.yahoo.com/screener/unsaved/e7370d23-8474-4f96-9775-57e532aa9fb0")
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
    google_url = 'https://news.google.com/rss/search?q={}'.format(ticker)
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

    dataframe = pd.DataFrame({'tweets': tweets, 'google news': google_news, 'yahoo news': yahoo_news})
    dataframe['tweets'] =  [re.sub(r'@[A-Za-z0-9]+','', str(x)) for x in dataframe['tweets']]
    dataframe['tweets'] =  [re.sub(r'^https?:\/\/.*[\r\n]*','', str(x)) for x in dataframe['tweets']]

    analyzer = SentimentIntensityAnalyzer()
    tweet_score = TextBlob(str(dataframe['tweets']))
    google_score = dataframe['google news'].apply(analyzer.polarity_scores).tolist()
    yahoo_score = dataframe['yahoo news'].apply(analyzer.polarity_scores).tolist()
    print(tweet_score)

    #tw_df = pd.DataFrame(tweet_score)
    g_df = pd.DataFrame(google_score)
    y_df = pd.DataFrame(yahoo_score)

    #tweet_mean = (tw_df['compound'].mean())
    tweet_mean = tweet_score.sentiment.polarity
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
    z = (round(float(300)/(y)))

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
            stop_loss=dict(stop_price=float(y)*float(1.005)),
            take_profit=dict(limit_price=(float(y)*float(1.02))))


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
            take_profit=dict(limit_price=(float(y)*float(1.005))))

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
