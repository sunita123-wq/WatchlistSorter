import json
import requests

# Load local watchlist.json
with open("watchlist.json", "r") as f:
    symbols = [line.strip() for line in f if line.strip()]

# TradingView Scan API Setup
payload = {
    "symbols": {
        "tickers": symbols,
        "query": {"types": []}
    },
    "columns": ["change"]
}

response = requests.post(
    "https://scanner.tradingview.com/india/scan",
    headers={
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json"
    },
    data=json.dumps(payload)
)

tv_data = response.json()

# Map symbol to change %
change_map = {item["s"]: item["d"][0] for item in tv_data.get("data", [])}

# Sort original symbols based on Change %
sorted_symbols = sorted(symbols, key=lambda s: change_map.get(s, -9999), reverse=True)

# Overwrite watchlist.json
with open("watchlist.json", "w") as f:
    for s in sorted_symbols:
        f.write(s + "\n")
