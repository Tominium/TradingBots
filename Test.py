from pattern.web import Twitter, plaintext, Newsfeed
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

res = requests.get("https://finance.yahoo.com/screener/unsaved/d2082756-0099-4dc1-b728-3a17ffe7bf49")
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
for tweets_list in twitter.search('$'+ticker, cached=False, count=5):
    print(plaintext(tweets_list.text))
    tweets.append(tweets_list.text)

df = pd.DataFrame({'tweets': tweets})
print(df)

analyzer = SentimentIntensityAnalyzer()
tweet_score = df['tweets'].apply(analyzer.polarity_scores).tolist()

print(tweet_score)
