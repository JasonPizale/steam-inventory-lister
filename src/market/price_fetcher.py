import requests
import time
import re
from utils.helpers import info, warn

def parse_price(price_str: str) -> float:
    """
    Convert Steam API price string to float.
    Handles USD, CAD, and other prefixes.
    """
    if not price_str:
        return 0.0
    # Remove anything that is not a digit, dot, or minus
    cleaned = re.sub(r"[^\d.]", "", price_str)
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def fetch_live_price(item: dict, currency=1, retries=3, delay=1) -> dict:
    """
    Fetch the live Steam Market price for a single item.
    currency: 1=USD, 20=CAD
    retries: number of times to retry on HTTP errors
    delay: seconds to wait between retries
    """
    market_hash_name = item.get("market_hash_name")
    appid = item.get("appid")
    url = (
        f"https://steamcommunity.com/market/priceoverview/"
        f"?appid={appid}&currency={currency}&market_hash_name={market_hash_name}"
    )

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 429:
                warn(f"HTTP 429 rate limit for {market_hash_name}, retrying ({attempt+1}/{retries})...")
                time.sleep(delay)
                continue
            if response.status_code != 200:
                warn(f"HTTP {response.status_code} for {market_hash_name}")
                return {"lowest_price": 0.0}
            data = response.json()
            if not data.get("success"):
                warn(f"Steam API returned failure for {market_hash_name}")
                return {"lowest_price": 0.0}
            
            price_str = data.get("lowest_price") or data.get("median_price")
            price_value = parse_price(price_str)
            return {"lowest_price": price_value}
        except Exception as e:
            warn(f"Error fetching price for {market_hash_name}: {e}")
            time.sleep(delay)
    
    warn(f"Failed to fetch price for {market_hash_name} after {retries} retries")
    return {"lowest_price": 0.0}

def merge_prices_with_inventory(items: list, price_map: dict) -> list:
    """Add the fetched prices back to the inventory items"""
    for item in items:
        key = item.get("market_hash_name")
        if key in price_map:
            item["lowest_price"] = price_map[key]
            item["recommended_price"] = price_map[key]
    return items
