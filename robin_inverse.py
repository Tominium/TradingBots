import pandas as pd
from yahoo_fin import stock_info as s
import alpaca_trade_api as tradeapi
from time import sleep

#authentication and connection details
api_key = 'PKFCU12STCW2UCJEW5FO'
api_secret = 'hBcrjfCn9ud3GSQqnsmw8CsWmWzRVDnyUn2i7S4b'
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
    sleep(time_to_open.total_seconds())

i = 0
def get_stock():
    global i
    df = pd.read_json('https://robintrack.net/api/largest_popularity_decreases?hours_ago=24&limit=50&percentage=false&min_popularity=50&start_index=0')
    robin_tracker = df.drop(['start_popularity', 'end_popularity'], axis=1)
    robin_tracker = robin_tracker[['symbol', 'name','popularity_difference']]
    print(robin_tracker)
    get_stock.ticker = robin_tracker.iloc[i,0]
    print(get_stock.ticker)
    i += 1
get_stock()

def check_price():
    ticker_price = s.get_live_price(get_stock.ticker)
    if ticker_price > 300:
        get_stock()
        check_price()
    elif ticker_price < 300:
        print(ticker_price)
check_price()

def get_order():
    try:
        y = s.get_live_price(get_stock.ticker)
        print(y)
        current_bal = account.cash
        print('Your Current Balance is {}'.format(current_bal))
        z = (round(float(300)/(y)))
        print("Positive Analysis")
        print('Buying {}'.format(get_stock.ticker))
        api.submit_order(symbol=get_stock.ticker,
            qty= z,
            side='buy',
            time_in_force='gtc',
            type='market',
            order_class='bracket',
            stop_loss=dict(stop_price=float(y)*float(0.995)),
            take_profit=dict(limit_price=(float(y)*float(1.005))))

    except Exception:
        get_stock()
        check_price()
        get_order()
        sleep(400)

get_order()

sleep(400)

def check_stocks():
    try:
        if len(api.list_positions()) == 0:
            get_stock()
            check_price()
            get_order()
            sleep(400)
            check_stocks()
        while len(api.list_positions()) != 0:
            pass
    except Exception:
        if len(api.list_positions()) == 0:
            get_stock()
            check_price()
            get_order()
            sleep(400)
            check_stocks()
        while len(api.list_positions()) != 0:
            pass
check_stocks()
