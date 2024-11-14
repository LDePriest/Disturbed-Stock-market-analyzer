from flask import Flask, request, jsonify
import data_fetcher
import analyzer
import storage
#has to be editing to run on http

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Stock Analyzer API! Use /analyze to get stock data."

@app.route('/analyze', methods=['GET'])
def analyze():
    symbols = request.args.get('symbols', '')
    stock_symbols = [symbol.strip().upper() for symbol in symbols.split(",") if symbol.strip()]

    if not stock_symbols:
        return jsonify({"error": "No valid stock symbols provided."}), 400

    results = {}
    for symbol in stock_symbols:
        try:
            data = data_fetcher.fetch_stock_data(symbol)
            if data is not None:
                analysis = analyzer.analyze_stock_data(data)
                storage.save_analysis(symbol, analysis)
                results[symbol] = analysis
            else:
                results[symbol] = {"error": "Failed to fetch data"}
        except Exception as exc:
            results[symbol] = {"error": str(exc)}
    
    return jsonify(results)

if __name__ == "__main__":
    # Make the server accessible on the network
    app.run(host='0.0.0.0', port=5000)
