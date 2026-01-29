import requests
import time
from typing import Dict, Any, Optional
from utils.helpers import info, warn

STEAM_PRICE_URL = "https://steamcommunity.com/market/priceoverview/"

# -----------------------------
# Core helpers
# -----------------------------

def fetch_price(
    url: str,
    session_headers: Dict[str, str],
    params: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    try:
        resp = requests.get(
            url,
            headers=session_headers,
            params=params,
            timeout=10
        )

        if resp.status_code == 429:
            handle_rate_limit(resp)
            return None

        if resp.status_code != 200:
            return None

        data = resp.json()
        if not data.get("success"):
            return None

        return data

    except Exception as e:
        warn(f"Price fetch failed: {e}")
        return None

def handle_rate_limit(response) -> None:
    if response.status_code == 429:
        warn("Rate limited by Steam, sleeping...")
        time.sleep(5)

def get_price_for_item(
    item: Dict[str, Any],
    session_headers: Dict[str, str]
) -> Optional[Dict[str, Any]]:
    name = item.get("market_hash_name")
    if not name:
        return None

    params = {
        "appid": item.get("appid", 730),
        "currency": 1,
        "market_hash_name": name,
    }

    raw = fetch_price(STEAM_PRICE_URL, session_headers, params)
    if not raw:
        return None

    return {
        "lowest_price": _clean_price(raw.get("lowest_price")),
        "median_price": _clean_price(raw.get("median_price")),
        "volume": raw.get("volume"),
    }

def build_price_map(
        inventory: list,
        session_headers: Dict[str, str],
        delay: float = 0.5
) -> Dict[str, Dict[str, Any]]:
    price_map = {}

    for item in inventory:
        name = item.get("market_hash_name")
        if not name:
            continue

        price = get_price_for_item(item, session_headers)
        if price:
            price_map[name] = price
        
        time.sleep(delay)

    return price_map

def merge_prices_with_inventory(inventory: list, price_map: Dict[str, Dict[str, Any]]) -> list:
    for item in inventory:
        name = item.get("market_hash_name")
        if name in price_map:
            item.update(price_map[name])
    return inventory

# -----------------------------
# Utils
# -----------------------------

def _clean_price(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    return float(
        value.replace("$", "")
            .replace(",", "")
            .strip()
    )