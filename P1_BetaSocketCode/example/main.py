# main.py
from flask import Flask, request, jsonify
from concurrent.futures import ProcessPoolExecutor, as_completed
import data_fetcher
import analyzer
import storage

app = Flask(__name__)

# Function to process each stock symbol, fetch and analyze data, and store results
def fetch_analyze_store(symbol):
    data = data_fetcher.fetch_stock_data(symbol)
    if data is not None:
        analysis = analyzer.analyze_stock_data(data)
        storage.save_analysis(symbol, analysis)
        return {"symbol": symbol, "analysis": analysis}
    return {"symbol": symbol, "error": "Failed to fetch data"}

# Endpoint for analyzing stocks
@app.route('/analyze', methods=['POST'])
def analyze_stocks():
    symbols = request.json.get("symbols", [])
    if not symbols:
        return jsonify({"error": "No stock symbols provided"}), 400

    results = []
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(fetch_analyze_store, symbol): symbol for symbol in symbols}
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                results.append({"symbol": futures[future], "error": str(exc)})
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
