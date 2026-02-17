from utils.helpers import prompt_sort_key

# -----------------------------
# Detect item category
# -----------------------------
def detect_category(item):
    """
    Returns a simple category string for an inventory item.
    Example categories: 'case', 'weapon skin', 'other'
    """
    item_type = item.get("type", "").lower()
    if "case" in item_type:
        return "case"
    elif "skin" in item_type or "weapon" in item_type:
        return "weapon skin"
    else:
        return "other"


# -----------------------------
# Apply filters
# -----------------------------
def apply_filters(inventory, categories=None, min_price=None, max_price=None, sort_key="price"):
    """
    Filters the inventory based on:
    - categories: list of allowed categories, or None for all
    - min_price: minimum price (inclusive)
    - max_price: maximum price (inclusive)
    - sort_key: "price" or "name"
    Returns a new list of filtered and sorted items.
    """
    filtered = []

    for item in inventory:
        if not item.get("marketable", True):
            continue

        category = detect_category(item)
        if categories and category not in categories:
            continue

        price = item.get("recommended_price", 0.0)
        if min_price is not None and price < min_price:
            continue
        if max_price is not None and price > max_price:
            continue

        filtered.append(item)

    # Sort
    if sort_key == "price":
        filtered.sort(key=lambda x: x.get("recommended_price", 0.0))
    elif sort_key == "name":
        filtered.sort(key=lambda x: x.get("market_hash_name", "").lower())

    return filtered


# -----------------------------
# Sort prompt (no game option)
# -----------------------------
def prompt_sort_key(allow_game=False):
    key = input(f"Sort by (price/name{'/game' if allow_game else ''}) [price]: ").strip().lower()
    if key not in ("price", "name") and (allow_game and key != "game"):
        return "price"
    return key
