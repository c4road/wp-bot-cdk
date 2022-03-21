from datetime import datetime, timedelta
import pandas as pd
from binance.client import Client as BinanceClient

from utils.secrets import get_binance_secret

interval_mapping = {
    "1MINUTE": BinanceClient.KLINE_INTERVAL_1MINUTE,
    "3MINUTE": BinanceClient.KLINE_INTERVAL_3MINUTE,
    "5MINUTE": BinanceClient.KLINE_INTERVAL_5MINUTE,
    "15MINUTE ": BinanceClient.KLINE_INTERVAL_15MINUTE,
    "30MINUTE ": BinanceClient.KLINE_INTERVAL_30MINUTE,
    "1HOUR": BinanceClient.KLINE_INTERVAL_1HOUR,
    "2HOUR": BinanceClient.KLINE_INTERVAL_2HOUR,
    "4HOUR": BinanceClient.KLINE_INTERVAL_4HOUR,
    "6HOUR": BinanceClient.KLINE_INTERVAL_6HOUR,
    "8HOUR": BinanceClient.KLINE_INTERVAL_8HOUR,
    "12HOUR ": BinanceClient.KLINE_INTERVAL_12HOUR ,
    "1DAY": BinanceClient.KLINE_INTERVAL_1DAY,
    "3DAY": BinanceClient.KLINE_INTERVAL_3DAY,
    "1WEEK": BinanceClient.KLINE_INTERVAL_1WEEK,
    "1MONTH": BinanceClient.KLINE_INTERVAL_1MONTH
}

def _get_client():
    try:
        client = BinanceClient(*get_binance_secret())
    except Exception:
        raise
    else:
        return client


def BinanceDataFrame(klines):
    asset = pd.DataFrame(klines,dtype=float, columns = (
        'Open Time',
        'Open',
        'High',
        'Low',
        'Close',
        'Volume',
        'Close time',
        'Quote asset volume',
        'Number of trades',
        'Taker buy base asset volume',
        'Taker buy quote asset volume',
        'Ignore'))

    asset['Datetime'] = pd.to_datetime(asset['Open Time'], unit='ms')
    asset.reset_index(drop=True, inplace=True)
    asset = asset.set_index('Datetime')

    return asset


def get_usdt_tickers(coins: list = None) -> list:
    """
    :param Client: Binance Client instance
    :param coins: A list of coin tickers
    :return list: a list of USDT based tickers given a list of coin tickers
    """
    client = _get_client()
    if not isinstance(coins, list):
        raise Exception('coins argument should be a list')
    try:
        all_ticker = client.get_all_tickers()
    except Exception as e:
        raise

    usd_tickers = []
    ticker_response = []

    for ticker in all_ticker:
        if ticker.get('symbol').endswith('USDT'):
            usd_tickers.append(ticker.get('symbol'))

    if not coins:
        return usd_tickers

    for ticker in usd_tickers:
        for coin in coins:
            if ticker.startswith(coin):
                if _is_usdt_valid(coin, ticker):
                    ticker_response.append(ticker)

    return ticker_response


def get_portfolio_data(tickers,
                       start_date,
                       end_date=None,
                       interval="1DAY"):
    """
    Example date format: December 1, 2021 UTC
    Example timestamp date format: 
    
        dt_string = '18/09/19 01:55:19'
        dt = datetime. strptime(dt_string, '%d/%m/%y %H:%M:%S')
        start = int(dt.timestamp() * 1000)
        
    Intervals: "1MINUTE", "3MINUTE", "5MINUTE", "15MINUTE ", "30MINUTE ", 
               "1HOUR", "2HOUR", "4HOUR", "6HOUR", "8HOUR", 
               "12HOUR ", "1DAY", "3DAY", "1WEEK", "1MONTH
               
    Default interval: "1DAY"
    
    """
    client = _get_client()
    tickers = get_usdt_tickers(client, tickers)
    
    if not isinstance(tickers, list):
        raise Exception(f"Invalid ticker format, should be list got {type(tickers)}")
    
    
    interval = interval_mapping.get(interval)
    if not interval:
        interval = interval_mapping["1DAY"]
    
    portfolio = pd.DataFrame()
    try:
        for asset in tickers:
            klines = client.get_historical_klines(
                symbol=asset, 
                interval=interval,
                start_str=start_date,
                end_str=end_date)
            closing_price = BinanceDataFrame(klines)['Close']
            portfolio[f"{asset.replace('USDT','')}"] = closing_price
    except Exception as e:
        raise

    return portfolio

def _is_usdt_valid(coin, ticker):
    allowed = ['BTC', 'ETH', 'BNB', 'ETH']
    if coin in allowed:
        if ticker != f'{coin}USDT':
            return False
    return True


def get_historical(coin,
                   start_date,
                   end_date=None,
                   interval="1DAY"):
    """
    Example date format: December 1, 2021 UTC
    Example timestamp date format: 
    
        dt_string = '18/09/19 01:55:19'
        dt = datetime. strptime(dt_string, '%d/%m/%y %H:%M:%S')
        start = int(dt.timestamp() * 1000)
        
    Intervals: "1MINUTE", "3MINUTE", "5MINUTE", "15MINUTE ", "30MINUTE ", 
               "1HOUR", "2HOUR", "4HOUR", "6HOUR", "8HOUR", 
               "12HOUR ", "1DAY", "3DAY", "1WEEK", "1MONTH
               
    Default interval: "1DAY"
    """
    client = _get_client()
    ticker = get_usdt_tickers(client, [coin])
    if not ticker:
        raise Exception("Ticker not found: {}".format(coin))
    if len(ticker) > 1:
        raise Exception("Multiple tickers found: {}".format(ticker))
    ticker = ticker.pop()
    interval = interval_mapping.get(interval)
    if not interval:
        interval = interval_mapping["1DAY"]
    
    data = pd.DataFrame()
    try:
        klines = client.get_historical_klines(
            symbol=ticker, 
            interval=interval,
            start_str=start_date,
            end_str=end_date)
        closing_price = BinanceDataFrame(klines)['Close']
    except Exception as e:
        raise
    data[f"{coin}"] = closing_price
    return data


def get_months_ago(coins, n=31):
    
    one_month_ago = datetime.today() - timedelta(days=n)
    one_month_ago = int(one_month_ago.timestamp() * 1000)
    
    return get_portfolio_data(coins,
                              one_month_ago)


def get_weeks_ago(coins, n=7):
    
    week_ago = datetime.today() - timedelta(days=n)
    week_ago = int(week_ago.timestamp() * 1000)
    
    return get_portfolio_data(coins,
                              week_ago)


def get_years_ago(coins, n=365):
    
    year_ago = datetime.today() - timedelta(days=n)
    year_ago = int(year_ago.timestamp() * 1000)
    
    return get_portfolio_data(coins,
                              year_ago)


def get_price_variation(interval, coins):
    
    handler = {
        'month': get_months_ago,
        'week': get_weeks_ago,
        'year': get_years_ago,
    }
    if interval not in handler.keys():
        raise Exception("[get_price_variation] Invalid interval {}".format(interval))
    
    data = handler[interval](coins)
    data = ((data.diff(len(data)-1).dropna() / data.iloc[-1:]) * 100).round(3)

    variations = {coin:variation[0] for coin, variation in data.iteritems()}

    return _prepare_variation_message(variations)


def _prepare_variation_message(variations):
    """
    Assemble variations and build a message to be send
    :param dict variations: dictionary with the variations eg. {'BTC': -3.5}
    """

    message = "\n".join("{} {}".format(k,v) for k,v in variations.items())

    return message
