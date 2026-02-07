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

def apply_filters(items, categories, min_price, max_price, sort_key=None, descending=False):
    """Apply category + price filters, then optional sorting"""
    items = filter_by_category(items, categories)
    items = filter_by_price(items, min_price, max_price)

    if sort_key:
        items = sort_items(items, sort_key, descending)

    return items

    for item in items:
        if "category" not in item:
            item["category"] = detect_category(item)

    if categories:
        categories = {c.lower() for c in categories}
        items = [
            item for item in items
            if item.get("category") in categories
        ]

