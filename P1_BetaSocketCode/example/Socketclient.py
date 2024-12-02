# client.py
import tkinter as tk
from tkinter import messagebox
import requests

SERVER_URL = "http://127.0.0.1:5000/analyze"

# Function to display results in the GUI
def display_results(results):
    results_text.delete("1.0", tk.END)  # Clear any previous results
    for result in results:
        symbol = result["symbol"]
        if "error" in result:
            results_text.insert(tk.END, f"{symbol}: {result['error']}\n")
        else:
            analysis = result["analysis"]
            results_text.insert(tk.END, f"{symbol}: 5min Moving Average = {analysis['5min_moving_average']}\n")

# Function to handle the button click and initiate stock analysis
def on_analyze_click(stock_entry):
    input_text = stock_entry.get()
    if not input_text:
        messagebox.showerror("Input Error", "Please enter at least one stock symbol.")
        return
    symbols = [symbol.strip().upper() for symbol in input_text.split(",")]

    try:
        response = requests.post(SERVER_URL, json={"symbols": symbols})
        response.raise_for_status()
        results = response.json()
        display_results(results)
    except requests.RequestException as e:
        messagebox.showerror("Network Error", str(e))

# Setting up the GUI
def setup_gui():
    root = tk.Tk()
    root.title("Distributed Stock Analyzer")

    # Label for instruction
    instruction_label = tk.Label(root, text="Enter stock symbols separated by commas (e.g., AAPL, GOOGL):")
    instruction_label.pack(pady=5)

    # Entry for stock symbols
    stock_entry = tk.Entry(root, width=50)
    stock_entry.pack(pady=5)

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
