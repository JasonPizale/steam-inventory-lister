"""
Utility functions for filtering and sorting Steam inventory items.
"""
from helpers import is_marketable

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

def apply_filters(items, categories, min_price, max_price, sort_key=None):
    """Apply category + price filters, then optional sorting"""
    items = filter_by_category(items, categories)
    items = filter_by_price(items, min_price, max_price)

    if sort_key:
        items = sort_items(items, sort_key, descending)

    return items

