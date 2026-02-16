import json
import urllib.parse
from typing import List, Dict, Any, Optional
from utils.helpers import info, warn

STEAM_SELL_URL = "https://steamcommunity.com/market/sellitem"

CATEGORY_PRICE_RULES = {
    "weapon skin": {"undercut": 0.02},
    "sticker": {"undercut": 0.01},
    "case": {"undercut": 0.00},
    "key": {"undercut": 0.01},
    "gloves": {"undercut": 0.02},
    "knife": {"undercut": 0.02},
}

def build_listing_queue(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    queue = []
    for item in items:
        if not item.get("marketable", True):
            continue
        price = calculate_recommended_price(item)
        if price is None:
            continue
        entry = {
            "market_hash_name": item.get("market_hash_name"),
            "appid": item.get("appid"),
            "contextid": item.get("contextid", "2"),
            "assetid": item.get("assetid"),
            "recommended_price": price,
            "category": item.get("category"),
            "sell_url": build_sell_url(item),
        }
        queue.append(entry)
    info(f"Built listing queue with {len(queue)} items")
    return queue

def calculate_recommended_price(item: Dict[str, Any]) -> Optional[float]:
    if item.get("recommended_price") is not None:
        return item["recommended_price"]
    lowest = item.get("lowest_price")
    category = item.get("category", "other").lower()
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
    name_encoded = urllib.parse.quote(item.get("market_hash_name", "UNKNOWN"))
    appid = item.get("appid")
    contextid = item.get("contextid", "2")
    assetid = item.get("assetid")
    price = item.get("recommended_price", 0)
    price_cents = int(round(price * 100))
    return f"{STEAM_SELL_URL}?appid={appid}&contextid={contextid}&assetid={assetid}&price={price_cents}&market_hash_name={name_encoded}"

def export_queue(queue: List[Dict[str, Any]], filepath: Optional[str] = None) -> None:
    if not filepath:
        return
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=4)
        info(f"Queue exported to {filepath}")
    except Exception as e:
        warn(f"Failed to export queue: {e}")
