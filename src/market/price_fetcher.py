import time
import requests
from typing import List, Dict, Any, Optional

STEAM_PRICE_URL = "https://steamcommunity.com/market/priceoverview/"

# -----------------------------
# Helpers
# -----------------------------
def _parse_price(value: str) -> float:
    """
    Convert Steam price string like '$2.34' or 'CDN$3.45' to float.
    """
    if not value:
        return 0.0
    try:
        return float(value.replace("$", "").replace("CDN", "").replace(",", "").strip())
    except:
        return 0.0

# -----------------------------
# Build price map
# -----------------------------
def build_price_map(
    inventory: List[Dict[str, Any]],
    live_fetch: bool = False,
    currency: int = 1,
    delay: float = 0.5
) -> Dict[str, float]:
    """
    Build a price map from inventory items.
    Options:
      - live_fetch=True: fetch prices from Steam Market
      - live_fetch=False: use 'recommended_price' in JSON or 0.0 as fallback
      - currency: 1=USD, 20=CAD
    """
    price_map = {}

    for item in inventory:
        market_hash_name = item.get("market_hash_name")
        if not market_hash_name:
            continue

        # fallback to recommended price
        price = item.get("recommended_price", 0.0)

        if live_fetch:
            try:
                params = {
                    "appid": item.get("appid", 730),
                    "currency": currency,
                    "market_hash_name": market_hash_name
                }
                resp = requests.get(STEAM_PRICE_URL, params=params, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    price = _parse_price(data.get("lowest_price"))
            except Exception:
                pass
            time.sleep(delay)

        price_map[market_hash_name] = price

    return price_map

# -----------------------------
# Merge prices with inventory
# -----------------------------
def merge_prices_with_inventory(
    inventory: List[Dict[str, Any]],
    price_map: Dict[str, float]
) -> List[Dict[str, Any]]:
    """
    Add 'recommended_price' to inventory items from price_map
    """
    for item in inventory:
        name = item.get("market_hash_name")
        item["recommended_price"] = price_map.get(name, 0.0)
    return inventory

# -----------------------------
# Direct execution guard
# -----------------------------
if __name__ == "__main__":
    print("This module should be imported, not executed directly.")