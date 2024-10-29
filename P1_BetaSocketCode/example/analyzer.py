# analyzer.py analyzes stock market

def analyze_stock_data(data):
    """Perform analysis on stock data."""
    closing_prices = data['Close'].tolist()
    if len(closing_prices) >= 5:
        moving_average = sum(closing_prices[-5:]) / 5
        return {"5min_moving_average": moving_average}
    return {"error": "Not enough data for analysis"}
