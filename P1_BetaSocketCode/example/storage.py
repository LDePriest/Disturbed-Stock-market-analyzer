# storage.py updates storage 

storage = {}

def save_analysis(symbol, analysis):
    """Store analysis results."""
    storage[symbol] = analysis
    print(f"Stored analysis for {symbol}: {analysis}")
