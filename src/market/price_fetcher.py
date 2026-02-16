import requests
import time
import re
from utils.helpers import warn, info

# -----------------------------
# Fetch live price with retries and parsing
# -----------------------------
def fetch_live_price(item, currency=1, max_retries=3, delay=1.0):
    """
    Fetches the lowest Steam Market price for an item.
    Handles CAD/USD conversion and HTTP 429 rate limiting.
    """
    market_name = item.get("market_hash_name")
    if not market_name:
        return {"lowest_price": 0.0}

    url = f"https://steamcommunity.com/market/priceoverview/?appid=730&currency={currency}&market_hash_name={market_name}"
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 429:
                warn(f"HTTP 429 rate limit for {market_name}, retrying ({attempt}/{max_retries})...")
                time.sleep(delay * attempt)  # incremental backoff
                continue
            data = response.json()
            
            price_str = data.get("lowest_price") or data.get("median_price") or "0"
            # Remove currency symbols and whitespace
            price_float = parse_price_string(price_str)
            return {"lowest_price": price_float}
        except Exception as e:
            warn(f"Attempt {attempt} failed for {market_name}: {e}")
            time.sleep(delay)
    warn(f"Failed to fetch price for {market_name} after {max_retries} retries")
    return {"lowest_price": 0.0}


# -----------------------------
# Merge fetched prices into inventory
# -----------------------------
def merge_prices_with_inventory(inventory, price_map):
    """
    Adds a 'recommended_price' field to each item based on price_map.
    """
    for item in inventory:
        market_name = item.get("market_hash_name")
        if market_name in price_map:
            item["recommended_price"] = price_map[market_name]
    return inventory


# -----------------------------
# Helpers
# -----------------------------
def parse_price_string(price_str):
    """
    Converts Steam Market price string to float.
    Handles formats like 'CDN 0.03', '$0.03', '0.03 USD', etc.
    """
    try:
        # Remove anything that's not a digit, dot, or minus
        cleaned = re.sub(r"[^\d.\-]", "", str(price_str))
        return float(cleaned)
    except Exception:
        return 0.0
