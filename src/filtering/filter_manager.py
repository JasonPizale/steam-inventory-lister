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

BROAD_CATEGORY_MAP = {
    "Rifle": "Weapon Skin",
    "Sniper Rifle": "Weapon Skin",
    "Pistol": "Weapon Skin",
    "SMG": "Weapon Skin",
    "Knife": "Weapon Skin",
    "Skin": "Weapon Skin",
    "Sticker": "Sticker",
    "Case": "Case",
    "Trading Card": "Trading Card",
}

def detect_category(item: dict) -> str:
    """
    Detects the broad category for a Steam Market item based on its name and type.
    """
    text = " ".join([
        str(item.get("market_hash_name", "")),
        str(item.get("type", "")),
        str(item.get("name", "")),
    ]).lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return BROAD_CATEGORY_MAP.get(category.capitalize(), "Other")
    return "Other"

def filter_by_category(items, categories):
    """Returns items that match given categories and are marketable"""
    if not categories:
        return [i for i in items if is_marketable(i)]

    return [
        i for i in items
        if is_marketable(i) and i.get("broad_category") in categories
    ]

def filter_by_price(items, min_price, max_price):
    """Return items with prices inside the min/max range"""
    filtered = []
    for item in items:
        price = item.get("recommended_price", 0)
        if (min_price is None or price >= min_price) and \
           (max_price is None or price <= max_price):
            filtered.append(item)
    return filtered

def sort_items(items, key, descending=False):
    """Sort items by price, name, or game"""
    sort_map = {
        "price": "recommended_price",
        "name": "market_hash_name",
        "game": "game_name",
    }
    field = sort_map.get(key)
    if not field:
        return items
    return sorted(items, key=lambda x: x.get(field, 0), reverse=descending)

def apply_filters(
    items,
    categories=None,
    min_price=None,
    max_price=None,
    sort_key="price",
    descending=False
):
    """Apply category + price filters, then optional sorting"""
    # Apply category + price
    filtered = [
        item for item in items
        if is_marketable(item) and
           (not categories or item.get("broad_category") in categories) and
           (min_price is None or item.get("recommended_price", 0) >= min_price) and
           (max_price is None or item.get("recommended_price", 0) <= max_price)
    ]

    # Apply sorting
    filtered = sort_items(filtered, sort_key, descending)
    return filtered
