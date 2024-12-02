import yfinance as yf
import ray

# Initialize Ray for distributed computing
ray.init()

@ray.remote
def fetch_stock_data(symbol):
    """
    Fetch stock data for a given symbol using Yahoo Finance.
    This function is remote-enabled for distributed execution.
    """
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d", interval="5m")  # 5-minute intervals for today
    if not data.empty:
        print(f"Fetched data for {symbol}")
        return symbol, data
    else:
        print(f"No data available for {symbol}")
        return symbol, None

def fetch_data_distributed(symbols):
    """
    Fetch stock data for a list of symbols using distributed computing with Ray.
    """
    futures = [fetch_stock_data.remote(symbol) for symbol in symbols]  # Call remote functions
    results = ray.get(futures)  # Wait for and fetch results from Ray
    return results

# Example usage
if __name__ == "__main__":
    stock_symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
    
    print("\nFetching data using distributed computing...")
    distributed_results = fetch_data_distributed(stock_symbols)
    print("Distributed Results:", distributed_results)
