# main.py
#how to run python main.py

from concurrent.futures import ProcessPoolExecutor, as_completed
import data_fetcher
import analyzer
import storage

STOCK_SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]

def main():
    with ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(fetch_analyze_store, symbol): symbol for symbol in STOCK_SYMBOLS
        }

        for future in as_completed(futures):
            symbol = futures[future]
            try:
                result = future.result()
                print(f"Completed processing for {symbol}: {result}")
            except Exception as exc:
                print(f"An error occurred with {symbol}: {exc}")

def fetch_analyze_store(symbol):
    """Fetch, analyze, and store data for a given stock symbol."""
    data = data_fetcher.fetch_stock_data(symbol)
    if data is not None:
        analysis = analyzer.analyze_stock_data(data)
        storage.save_analysis(symbol, analysis)
        return analysis
    return {"error": "Failed to fetch data"}

if __name__ == "__main__":
    main()
