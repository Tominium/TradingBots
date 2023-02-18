from pattern.web import Twitter, plaintext, Newsfeed
import pandas as pd
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import alpaca_trade_api as tradeapi
from time import sleep
from yahoo_fin import stock_info as s
from finviz.screener import Screener

#authentication and connection details
api_key = 'PKHYSJ8GOOSI1RAGJBJQ'
api_secret = 'VsrFm4cJWjgLnnEwAK8TaA2xCO1rRc9egnQo0yox'
base_url = 'https://paper-api.alpaca.markets'

#instantiate REST API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')
account = api.get_account()
print(account)

clock = api.get_clock()
if clock.is_open:
    pass
else:
    time_to_open = clock.next_open - clock.timestamp
    sleep(time_to_open.total_seconds() + 300)

i = 0
def get_stock():
    global i
    filters = ['sh_float_u10', 'sh_insiderown_o20', 'sh_price_u10']  # Shows companies in NASDAQ which are in the S&P500
    stock_list = Screener(filters=filters, table='Overview')  # Get the performance table and sort it by price ascending

    # Print the table into the console
    print(stock_list)
    ticker = stock_list[i]['Ticker']
    print(ticker)

    i += 1

    tweets = []
    twitter = Twitter(language='en')
    for tweets_list in twitter.search('$'+ticker, cached=False, count=100):
        tweets.append(tweets_list.text)
        print(plaintext(tweets_list.text))


    print('----------------------')

    google_news = []
    google_url = 'https://news.google.com/rss/search?q={}'.format(ticker)
    for google_result in Newsfeed().search(google_url)[:100]:
        google_news.append(google_result.title)
        print(plaintext(google_result.title))

    print('----------------------')

    yahoo_news = []
    yahoo_url = 'http://finance.yahoo.com/rss/headline?s={}'.format(ticker)
    for yahoo_result in Newsfeed().search(yahoo_url)[:100]:
        yahoo_news.append(yahoo_result.title)
        print(plaintext(yahoo_result.title))

    print('----------------------')

    print(tweets)
    print(yahoo_news)
    print(google_news)

    tweets =  [re.sub(r'@[A-Za-z0-9]+','', str(x)) for x in tweets]
    tweets =  [re.sub(r'^https?:\/\/.*[\r\n]*','', str(x)) for x in tweets]

    analyzer = SentimentIntensityAnalyzer()
    tweet_score = analyzer.polarity_scores((tweets))
    google_score = analyzer.polarity_scores(google_news)
    yahoo_score = analyzer.polarity_scores(yahoo_news)
    print(tweet_score)

    tw_df = pd.DataFrame(tweet_score, index=[0])
    g_df = pd.DataFrame(google_score, index=[0])
    y_df = pd.DataFrame(yahoo_score, index=[0])

    tweet_mean = (tw_df['compound'].mean())
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

    try:
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
                stop_loss=dict(stop_price=float(y)*float(0.99)),
                take_profit=dict(limit_price=(float(y)*float(1.01))))

        elif mean <= 0.10:
            get_stock()

    except Exception():
        get_stock()

get_stock()

sleep(400)

def check_stocks():
    try:
    	if len(api.list_positions()) == 0:
    		print("none")
    		get_stock()
    		sleep(400)
    		check_stocks()
    	while len(api.list_positions()) != 0:
    		pass
    except Exception:
    	if len(api.list_positions()) == 0:
    		print("none")
    		get_stock()
    		sleep(400)
    		check_stocks()
    	while len(api.list_positions()) != 0:
    		pass
check_stocks()
