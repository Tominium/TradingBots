from pattern.web import Twitter, plaintext, Newsfeed
import pandas as pd
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from yahoo_fin import stock_info as s
import re
from time import sleep
# Oanda Packages
from oandapyV20 import API
import oandapyV20
from oandapyV20.contrib.requests import MarketOrderRequest
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.accounts as accounts
import tkinter as tk

r = tk.Tk()

def whole_thing():
    global r
    api = oandapyV20.API(environment="practice", access_token="c46ba9f76a6418d2359850b5421abc96-a108d8c829989f6122465e5420468636")

    def eur_usd():

        ticker = 'EUR/USD'

        tweets = []
        twitter = Twitter(language='en')
        for tweets_list in twitter.search(ticker, cached=False, count=100):
            tweets.append(tweets_list.text)

        google_news = []
        google_url = 'https://news.google.com/rss/search?q={}'.format(ticker)
        for google_result in Newsfeed().search(google_url)[:100]:
            google_news.append(google_result.title)

        reddit_news = []
        reddit_url = 'https://www.reddit.com/search.rss?q={}&sort=relevance&type=link'.format(ticker)
        for reddit_result in Newsfeed().search(reddit_url)[:100]:
            reddit_news.append(reddit_result.title)

        tweets =  [re.sub(r'@[A-Za-z0-9]+','', str(x)) for x in tweets]
        tweets =  [re.sub(r'^https?:\/\/.*[\r\n]*','', str(x)) for x in tweets]

        analyzer = SentimentIntensityAnalyzer()
        tweet_score = analyzer.polarity_scores((tweets))
        google_score = analyzer.polarity_scores(google_news)
        reddit_score = analyzer.polarity_scores(reddit_news)
        print(tweet_score)

        tw_df = pd.DataFrame(tweet_score, index=[0])
        g_df = pd.DataFrame(google_score, index=[0])
        r_df = pd.DataFrame(reddit_score, index=[0])

        tweet_mean = (tw_df['compound'].mean())
        google_mean = (g_df['compound'].mean())
        reddit_mean = (r_df['compound'].mean())

        combined_mean = tweet_mean + google_mean + reddit_mean
        eur_usd.mean = round((combined_mean/3), 2)
    eur_usd()

    def aud_usd():

        ticker = 'AUD/USD'

        tweets = []
        twitter = Twitter(language='en')
        for tweets_list in twitter.search(ticker, cached=False, count=100):
            tweets.append(tweets_list.text)

        google_news = []
        google_url = 'https://news.google.com/rss/search?q={}'.format(ticker)
        for google_result in Newsfeed().search(google_url)[:100]:
            google_news.append(google_result.title)

        reddit_news = []
        reddit_url = 'https://www.reddit.com/search.rss?q={}&sort=relevance&type=link'.format(ticker)
        for reddit_result in Newsfeed().search(reddit_url)[:100]:
            reddit_news.append(reddit_result.title)

        tweets =  [re.sub(r'@[A-Za-z0-9]+','', str(x)) for x in tweets]
        tweets =  [re.sub(r'^https?:\/\/.*[\r\n]*','', str(x)) for x in tweets]

        analyzer = SentimentIntensityAnalyzer()
        tweet_score = analyzer.polarity_scores((tweets))
        google_score = analyzer.polarity_scores(google_news)
        reddit_score = analyzer.polarity_scores(reddit_news)
        print(tweet_score)

        tw_df = pd.DataFrame(tweet_score, index=[0])
        g_df = pd.DataFrame(google_score, index=[0])
        r_df = pd.DataFrame(reddit_score, index=[0])

        tweet_mean = (tw_df['compound'].mean())
        google_mean = (g_df['compound'].mean())
        reddit_mean = (r_df['compound'].mean())

        combined_mean = tweet_mean + google_mean + reddit_mean
        aud_usd.mean = round((combined_mean/3), 2)
    aud_usd()

    def eur_cad():

        ticker = 'EUR/CAD'

        tweets = []
        twitter = Twitter(language='en')
        for tweets_list in twitter.search(ticker, cached=False, count=100):
            tweets.append(tweets_list.text)

        google_news = []
        google_url = 'https://news.google.com/rss/search?q={}'.format(ticker)
        for google_result in Newsfeed().search(google_url)[:100]:
            google_news.append(google_result.title)

        reddit_news = []
        reddit_url = 'https://www.reddit.com/search.rss?q={}&sort=relevance&type=link'.format(ticker)
        for reddit_result in Newsfeed().search(reddit_url)[:100]:
            reddit_news.append(reddit_result.title)

        tweets =  [re.sub(r'@[A-Za-z0-9]+','', str(x)) for x in tweets]
        tweets =  [re.sub(r'^https?:\/\/.*[\r\n]*','', str(x)) for x in tweets]

        analyzer = SentimentIntensityAnalyzer()
        tweet_score = analyzer.polarity_scores((tweets))
        google_score = analyzer.polarity_scores(google_news)
        reddit_score = analyzer.polarity_scores(reddit_news)
        print(tweet_score)

        tw_df = pd.DataFrame(tweet_score, index=[0])
        g_df = pd.DataFrame(google_score, index=[0])
        r_df = pd.DataFrame(reddit_score, index=[0])

        tweet_mean = (tw_df['compound'].mean())
        google_mean = (g_df['compound'].mean())
        reddit_mean = (r_df['compound'].mean())

        combined_mean = tweet_mean + google_mean + reddit_mean
        eur_cad.mean = round((combined_mean/3), 2)
    eur_cad()

    def usd_mxn():

        ticker = 'USD/MXN'

        tweets = []
        twitter = Twitter(language='en')
        for tweets_list in twitter.search(ticker, cached=False, count=100):
            tweets.append(tweets_list.text)

        google_news = []
        google_url = 'https://news.google.com/rss/search?q={}'.format(ticker)
        for google_result in Newsfeed().search(google_url)[:100]:
            google_news.append(google_result.title)

        reddit_news = []
        reddit_url = 'https://www.reddit.com/search.rss?q={}&sort=relevance&type=link'.format(ticker)
        for reddit_result in Newsfeed().search(reddit_url)[:100]:
            reddit_news.append(reddit_result.title)

        tweets =  [re.sub(r'@[A-Za-z0-9]+','', str(x)) for x in tweets]
        tweets =  [re.sub(r'^https?:\/\/.*[\r\n]*','', str(x)) for x in tweets]

        analyzer = SentimentIntensityAnalyzer()
        tweet_score = analyzer.polarity_scores((tweets))
        google_score = analyzer.polarity_scores(google_news)
        reddit_score = analyzer.polarity_scores(reddit_news)
        print(tweet_score)

        tw_df = pd.DataFrame(tweet_score, index=[0])
        g_df = pd.DataFrame(google_score, index=[0])
        r_df = pd.DataFrame(reddit_score, index=[0])

        tweet_mean = (tw_df['compound'].mean())
        google_mean = (g_df['compound'].mean())
        reddit_mean = (r_df['compound'].mean())

        combined_mean = tweet_mean + google_mean + reddit_mean
        usd_mxn.mean = round((combined_mean/3), 2)
    usd_mxn()

    def nzd_usd():

        ticker = 'NZD/USD'

        tweets = []
        twitter = Twitter(language='en')
        for tweets_list in twitter.search(ticker, cached=False, count=100):
            tweets.append(tweets_list.text)

        google_news = []
        google_url = 'https://news.google.com/rss/search?q={}'.format(ticker)
        for google_result in Newsfeed().search(google_url)[:100]:
            google_news.append(google_result.title)

        reddit_news = []
        reddit_url = 'https://www.reddit.com/search.rss?q={}&sort=relevance&type=link'.format(ticker)
        for reddit_result in Newsfeed().search(reddit_url)[:100]:
            reddit_news.append(reddit_result.title)

        tweets =  [re.sub(r'@[A-Za-z0-9]+','', str(x)) for x in tweets]
        tweets =  [re.sub(r'^https?:\/\/.*[\r\n]*','', str(x)) for x in tweets]

        analyzer = SentimentIntensityAnalyzer()
        tweet_score = analyzer.polarity_scores((tweets))
        google_score = analyzer.polarity_scores(google_news)
        reddit_score = analyzer.polarity_scores(reddit_news)
        print(tweet_score)

        tw_df = pd.DataFrame(tweet_score, index=[0])
        g_df = pd.DataFrame(google_score, index=[0])
        r_df = pd.DataFrame(reddit_score, index=[0])

        tweet_mean = (tw_df['compound'].mean())
        google_mean = (g_df['compound'].mean())
        reddit_mean = (r_df['compound'].mean())

        combined_mean = tweet_mean + google_mean + reddit_mean
        nzd_usd.mean = round((combined_mean/3), 2)
    nzd_usd()

    def get_order():
        all_mean = [eur_usd.mean, aud_usd.mean, eur_cad.mean, nzd_usd.mean, usd_mxn.mean]
        greatest = max(all_mean)
        print(greatest)

        if greatest == eur_usd.mean:
            ticker = 'EUR_USD'
            symbol = 'EURUSD=X'
        elif greatest == aud_usd.mean:
            ticker = 'AUD_USD'
            symbol = 'AUDUSD=X'
        elif greatest == eur_cad.mean:
            ticker = "EUR_CAD"
            symbol = 'EURCAD=X'
        elif greatest == nzd_usd.mean:
            ticker = "NZD_USD"
            symbol = 'NZDUSD=X'
        elif greatest == usd_mxn.mean:
            ticker = "USD_MXN"
            symbol = 'MXN=X'

        accountID = "101-001-15461966-001"
        print(symbol)
        price = s.get_live_price(symbol)
        print(price)
        quantity = round(50/float(price))

        if greatest >= 0.10:
            print("Positive")
            print(("Buying {}".format(ticker)))
            label1 = tk.Label(r, text=("Buying {}".format(ticker)))
            label1.pack(fill='both', expand=True, padx=20, pady=20)
            buying = MarketOrderRequest(instrument=ticker,
             units=quantity,
             takeProfitOnFill=TakeProfitDetails(price=price*1.002).data,
             stopLossOnFill=StopLossDetails(price=price*.998).data)
            p = orders.OrderCreate(accountID, data=buying.data)
            api.request(p)

        elif greatest <= 0.09:
            print('Negative')
            print("Shorting {}".format(ticker))
            label1 = tk.Label(r, text=("Shorting {}".format(ticker)))
            label1.pack(fill='both', expand=True, padx=20, pady=20)
            shorting = MarketOrderRequest(instrument=ticker,
             units= (quantity * -1),
             takeProfitOnFill=TakeProfitDetails(price=price*.998).data,
             stopLossOnFill=StopLossDetails(price=price*1.002).data)
            p = orders.OrderCreate(accountID, data=shorting.data)
            api.request(p)

    get_order()

r.title('Forex Bot')
r.geometry('500x250')
button = tk.Button(r, text='Start Bot', width='25', command=whole_thing)
button.pack(fill='both', expand=True, padx=20, pady=20)
r.mainloop()
