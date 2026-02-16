"""
Utility functions for filtering and sorting Steam inventory items.
"""
from utils.helpers import is_marketable

CATEGORY_KEYWORDS = {
    "card": ["trading card"],
    "booster": ["booster pack"],
    "sticker": ["sticker"],
    "case": ["case", "crate"],
    "key": ["key"],
    "agent": ["agent"],
    "weapon": ["weapon", "rifle", "pistol", "knife", "skin"],
    "cosmetic": ["hat", "cosmetic", "wearable"],
    "tool": ["tool"],
    "bundle": ["bundle", "set"],
}

def detect_category(item: dict) -> str:
    """
    Detects the category for a steam market item based on its name and type.
    """
    text = " ".join([
        str(item.get("market_hash_name", "")),
        str(item.get("type", "")),
        str(item.get("name", "")),
    ]).lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return category

    return "other"

def filter_by_category(items, categories):
    """Returns items that match given categories and are marketable"""
    if not categories:
        return [i for i in items if is_marketable(i)]

    return [
        i for i in items
        if is_marketable(i) and i.get("type") in categories
    ]

def filter_by_price(items, min_price, max_price):
    """Return items with prices inside the min/max range"""
    filtered = []
    for item in items:
        price = item.get("lowest_price")
        if price is None:
            continue
        if (min_price is None or price >= min_price) and \
            (max_price is None or price <= max_price):
            filtered.append(item)
    return filtered 

def sort_items(items, key, descending=False):
    """Sort items by price, name, or game"""
    sort_map = {
        "price": "lowest_price",
        "name": "name",
        "game": "game",
    }
    field = sort_map.get(key)
    if not field:
        return items
    
    return sorted(items, key=lambda x: x.get(field), reverse=descending)

def apply_filters(
    items,
    categories=None,
    min_price=None,
    max_price=None,
    sort_key=None,
    descending=False
):
    """Apply category + price filters, then optional sorting"""
    filtered = []

    for item in items:
        price = item.get("recommended_price", 0)

        # Category filter
        if categories and item.get("category") not in categories:
            continue

        # Min price
        if min_price is not None and price < min_price:
            continue

        # Max price
        if max_price is not None and price > max_price:
            continue

        filtered.append(item)

    # Sorting
    if sort_key == "price":
        filtered.sort(key=lambda x: x.get("recommended_price", 0), reverse=True)
    elif sort_key == "name":
        filtered.sort(key=lambda x: x.get("market_hash_name", ""))

    return filtered