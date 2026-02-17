import requests
import time
import re
from utils.helpers import warn, info

# -----------------------------
# Helpers
# -----------------------------
def clean_steam_price(price_string):
    """
    Converts Steam Market price string to float safely.
    Handles formats like "$0.03", "CDN$ 5.44", "$1,234.56" etc.
    """
    if not price_string:
        return 0.0

    # Remove everything except digits, dot, comma, minus
    cleaned = re.sub(r"[^\d.,\-]", "", str(price_string))

    # Remove thousands separators
    cleaned = cleaned.replace(",", "")

    try:
        return float(cleaned)
    except ValueError:
        return 0.0

# -----------------------------
# Fetch live price with retries and parsing
# -----------------------------
def fetch_live_price(item, currency=1, max_retries=5, delay=1.0):
    """
    Fetches the lowest Steam Market price for an item.
    Handles CAD/USD conversion and HTTP 429 rate limiting with exponential backoff.
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
                time.sleep(delay * (2 ** (attempt - 1)))  # exponential backoff: 1,2,4,8,16
                continue

            data = response.json()
            lowest_price_raw = data.get("lowest_price") or data.get("median_price") or "0"

            # Clean price string and convert to float
            lowest_price = clean_steam_price(lowest_price_raw)

            return {"lowest_price": lowest_price}

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
    Adds a 'computed_price' field to each item based on price_map.
    """
    for item in inventory:
        market_name = item.get("market_hash_name")
        if market_name in price_map:
            item["computed_price"] = price_map[market_name]
        else:
            # fallback to recommended price if fetch failed
            item["computed_price"] = item.get("recommended_price", 0.0)
    return inventory
