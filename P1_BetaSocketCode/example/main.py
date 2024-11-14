import tkinter as tk
from tkinter import messagebox
from concurrent.futures import ProcessPoolExecutor, as_completed
import data_fetcher
import analyzer
import storage

STOCK_SYMBOLS = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "FXAIX"]

# Function to process each stock symbol, fetch and analyze data, and store results
def fetch_analyze_store(symbol):
    data = data_fetcher.fetch_stock_data(symbol)
    if data is not None:
        analysis = analyzer.analyze_stock_data(data)
        storage.save_analysis(symbol, analysis)
        return symbol, analysis
    return symbol, {"error": "Failed to fetch data"}

# GUI function to get stock symbols, fetch data, and display results
def analyze_stocks(symbols):
    results = {}
    with ProcessPoolExecutor() as executor:
        futures = {
            executor.submit(fetch_analyze_store, symbol): symbol for symbol in symbols
        }
        for future in as_completed(futures):
            symbol = futures[future]
            try:
                symbol, result = future.result()
                results[symbol] = result
            except Exception as exc:
                results[symbol] = {"error": str(exc)}
    
    display_results(results)

# Function to display results in the GUI
def display_results(results):
    results_text.delete("1.0", tk.END)  # Clear any previous results
    for symbol, analysis in results.items():
        if "error" in analysis:
            results_text.insert(tk.END, f"{symbol}: {analysis['error']}\n")
        else:
            results_text.insert(tk.END, f"{symbol}: 5min Moving Average = {analysis['5min_moving_average']}\n")

# Function to handle the button click and initiate stock analysis
def on_analyze_click(stock_entry):
    input_text = stock_entry.get()
    if not input_text:
        messagebox.showerror("Input Error", "Please enter at least one stock symbol.")
        return
    symbols = [symbol.strip().upper() for symbol in input_text.split(",")]
    analyze_stocks(symbols)

# Setting up the GUI
def setup_gui():
    root = tk.Tk()
    root.title("Stock Analyzer")

    # Label for instruction
    instruction_label = tk.Label(root, text="Enter stock symbols separated by commas (e.g., AAPL, GOOGL):")
    instruction_label.pack(pady=5)

    # Entry for stock symbols
    stock_entry = tk.Entry(root, width=50)
    stock_entry.pack(pady=5)
    stock_entry.insert(0, ", ".join(STOCK_SYMBOLS))  # Default symbols

    # Button to start analysis
    analyze_button = tk.Button(root, text="Analyze Stocks", command=lambda: on_analyze_click(stock_entry))
    analyze_button.pack(pady=10)

    # Text box to display results
    global results_text
    results_text = tk.Text(root, height=15, width=60)
    results_text.pack(pady=10)

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    setup_gui()
