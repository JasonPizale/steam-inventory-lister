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
    "weapon skin": ["rifle", "sniper rifle", "pistol", "knife", "weapon", "skin", "gloves"],
    "cosmetic": ["hat", "cosmetic", "wearable"],
    "tool": ["tool"],
    "bundle": ["bundle", "set"],
}

def detect_category(item: dict) -> str:
    """
    Detects the category for a Steam Market item based on its name and type.
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


def apply_filters(
    items,
    categories=None,
    min_price=None,
    max_price=None,
    sort_key="price",
    descending=False
):
    """Apply category + price filters, then sorting"""
    filtered = []

    for item in items:
        price = item.get("recommended_price", 0)
        item_category = item.get("category", detect_category(item))

        # Category filter
        if categories and item_category not in categories:
            continue

        # Price filters
        if (min_price is not None and price < min_price) or \
           (max_price is not None and price > max_price):
            continue

        # Only include marketable items
        if not is_marketable(item):
            continue

        # Store detected category for queue
        item["category"] = item_category
        filtered.append(item)

    # Sorting
    if sort_key == "price":
        filtered.sort(key=lambda x: x.get("recommended_price", 0), reverse=descending)
    elif sort_key == "name":
        filtered.sort(key=lambda x: x.get("market_hash_name", "").lower())
    elif sort_key == "game":
        filtered.sort(key=lambda x: x.get("game", "").lower())

    return filtered
