# data_fetcher.py fetches data 

import yfinance as yf

def fetch_stock_data(symbol):
    """Fetch stock data for a given symbol using Yahoo Finance."""
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d", interval="5m")  # 5-minute intervals for today
    if not data.empty:
        return data
    else:
        return None
