import json
from typing import List, Dict, Any, Optional
from utils.helpers import info, warn

STEAM_SELL_URL = "https://steamcommunity.com/market/sellitem"

CATEGORY_PRICE_RULES = {
    "trading_card": {"undercut": 0.01},
    "sticker": {"undercut": 0.01},
    "case": {"undercut": 0.00},
    "skin": {"undercut": 0.02},
}


# -----------------------------
# Core Queue Functions
# -----------------------------

def build_listing_queue(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Build a listing-ready queue from filtered inventory items
    """
    queue = []

    for item in items:
        price = calculate_recommended_price(item)
        if price is None:
            continue

        entry = {
            "market_hash_name": item.get("market_hash_name"),
            "appid": item.get("appid"),
            "contextid": item.get("contextid", "2"),
            "assetid": item.get("assetid"),
            "lowest_price": item.get("lowest_price"),
            "recommended_price": price,
            "volume": item.get("volume"),
            "sell_url": build_sell_url(item),
        }

        queue.append(entry)
    
    info(f"Built listing queue with {len(queue)} items")
    return queue

def calculate_recommended_price(item: Dict[str, Any]) -> Optional[float]:
    """
    Calculate recommended listing price based on lowest market price
    """
    lowest = item.get("lowest_price")
    category = item.get("category", "other")

    if lowest is None:
        return None
    
    rule = CATEGORY_PRICE_RULES.get(category, {"undercut": 0.01})

    if rule.get("skip"):
        return None

    recommended = round(lowest - rule["undercut"], 2)

    if recommended <= 0:
        return None

    return recommended

def build_sell_url(item: Dict[str, Any]) -> str:
    """
    Build Steam Market sell URL for the item
    """
    return (
        f"{STEAM_SELL_URL}"
        f"?appid={item.get('appid')}"
        f"&contextid={item.get('contextid', '2')}"
        f"&assetid={item.get('assetid')}"
    )

def export_queue(queue: List[Dict[str, Any]], filepath: Optional[str] = None) -> None:
    """
    Export queue to JSON file if filepath is provided
    """
    if not filepath:
        return

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=4)
        info(f"Queue exported to {filepath}")
    except Exception as e:
        warn(f"Failed to export queue: {e}")