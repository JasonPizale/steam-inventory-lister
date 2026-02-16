from utils.helpers import is_marketable

CATEGORY_KEYWORDS = {
    "card": ["trading card"],
    "booster": ["booster pack"],
    "sticker": ["sticker"],
    "case": ["case", "crate"],
    "key": ["key"],
    "agent": ["agent"],
    "weapon skin": ["weapon", "rifle", "sniper rifle", "pistol", "knife", "skin"],
    "cosmetic": ["hat", "cosmetic", "wearable"],
    "tool": ["tool"],
    "bundle": ["bundle", "set"],
}

def detect_category(item: dict) -> str:
    text = " ".join([str(item.get("market_hash_name", "")),
                     str(item.get("type", "")),
                     str(item.get("name", ""))]).lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return category
    return "other"

def apply_filters(items, categories=None, min_price=None, max_price=None, sort_key=None):
    filtered = []
    for item in items:
        if not is_marketable(item):
            continue
        price = item.get("recommended_price", 0)
        cat = item.get("category", detect_category(item))
        if categories and cat not in categories:
            continue
        if min_price is not None and price < min_price:
            continue
        if max_price is not None and price > max_price:
            continue
        item["category"] = cat
        filtered.append(item)

    if sort_key == "price":
        filtered.sort(key=lambda x: x.get("recommended_price", 0), reverse=True)
    elif sort_key == "name":
        filtered.sort(key=lambda x: x.get("market_hash_name", ""))
    elif sort_key == "game":
        filtered.sort(key=lambda x: x.get("game", ""))
    return filtered
