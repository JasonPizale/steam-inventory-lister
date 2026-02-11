# price_fetcher.py
from typing import List, Dict, Any

# -----------------------------
# Build price map
# -----------------------------
def build_price_map(inventory: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Build a price map from inventory items.

    Since we are not fetching live prices, use either:
    - pre-filled 'recommended_price' in the JSON
    - fallback to 0 if not present
    """
    price_map = {}
    for item in inventory:
        market_hash_name = item.get("market_hash_name")
        recommended_price = item.get("recommended_price", 0.0)
        if market_hash_name:
            price_map[market_hash_name] = recommended_price
    return price_map

# -----------------------------
# Merge prices with inventory
# -----------------------------
def merge_prices_with_inventory(
    inventory: List[Dict[str, Any]],
    price_map: Dict[str, float]
) -> List[Dict[str, Any]]:
    """
    Add 'recommended_price' field to each inventory item from price_map.
    """
    for item in inventory:
        market_hash_name = item.get("market_hash_name")
        item["recommended_price"] = price_map.get(market_hash_name, 0.0)
    return inventory

# -----------------------------
# Direct execution guard
# -----------------------------
if __name__ == "__main__":
    print("This module should be imported, not executed directly.")
