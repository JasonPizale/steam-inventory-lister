import time
import json
import os
from math import ceil
from market import price_fetcher

# ==============================
# CONFIGURATION / SETTINGS
# ==============================
CURRENCY_OPTIONS = {1: 'USD', 2: 'CAD'}

RETRY_LIMIT = 3
DELAY_BETWEEN_ITEMS = 0.1
DELAY_BETWEEN_BATCHES = 2
BATCH_SIZE = 20
DELAY_ON_429 = 1

CACHE_FILE = "price_cache.json"

# ==============================
# CACHE UTILITIES
# ==============================

def load_cache():
    """
    "Load cached prices from disk"
    """
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    """
    "Save cached prices to disk"
    """
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=4)

# ==============================
# PRICE FETCHING
# ==============================

def fetch_item_price(item, currency_id, cache):
    """
    "Fetch single item price with retry, rate-limit handling, and cache fallback"
    """
    name = item["market_hash_name"]

    # ✅ Check cache first
    if name in cache:
        print(f"[INFO] Using cached price for {name}: {cache[name]}")
        return cache[name]

    for attempt in range(RETRY_LIMIT):
        try:
            price_info = price_fetcher.fetch_live_price(item, currency=currency_id)
            price_str = price_info.get("lowest_price", "0") or "0"

            # Clean price string
            price_float = float(
                price_str
                .replace("CDN$", "")
                .replace("$", "")
                .replace("USD", "")
                .strip()
            )

            print(f"[INFO] Fetched price for {name}: {price_float}")

            # Save to cache
            cache[name] = price_float
            save_cache(cache)

            return price_float

        except ValueError:
            print(f"[WARN] Could not parse price for {name}")
            return 0.0

        except price_fetcher.HTTP429Error:
            wait_time = DELAY_ON_429 * (2 ** attempt)
            print(f"[WARN] HTTP 429 for {name}, retrying in {wait_time}s...")
            time.sleep(wait_time)
            continue

        except Exception as e:
            print(f"[WARN] Failed to fetch price for {name}: {e}")
            break

    # ✅ Fallback to cache if available
    if name in cache:
        print(f"[INFO] Using cached fallback for {name}: {cache[name]}")
        return cache[name]

    print(f"[WARN] Failed to fetch price for {name} after retries")
    return 0.0

def fetch_inventory_prices(inventory, currency_id):
    """
    "Fetch all prices using batching, throttling, and caching"
    """
    prices = {}
    cache = load_cache()

    total_items = len(inventory)
    total_batches = ceil(total_items / BATCH_SIZE)

    for batch_index in range(total_batches):
        start = batch_index * BATCH_SIZE
        end = start + BATCH_SIZE
        batch = inventory[start:end]

        print(f"\n[INFO] Fetching batch {batch_index + 1}/{total_batches}...")

        for item in batch:
            prices[item["market_hash_name"]] = fetch_item_price(
                item,
                currency_id,
                cache
            )
            time.sleep(DELAY_BETWEEN_ITEMS)

        print(f"[INFO] Batch {batch_index + 1} complete. Waiting {DELAY_BETWEEN_BATCHES}s...")
        time.sleep(DELAY_BETWEEN_BATCHES)

    return prices

# ==============================
# MAIN LOOP
# ==============================

def run():
    print("Select currency:")
    for key, val in CURRENCY_OPTIONS.items():
        print(f"{key}) {val}")

    choice = input("Choice (1 or 2, default 1): ").strip()
    currency_id = int(choice) if choice in ["1", "2"] else 1

    print(f"Fetching live prices in {CURRENCY_OPTIONS[currency_id]}...")

    inventory = price_fetcher.get_inventory()

    prices = fetch_inventory_prices(inventory, currency_id)

    print("\n[INFO] Final fetched prices:")
    for name, price in prices.items():
        print(f"{name}: {price}")

# ==============================
# ENTRY POINT
# ==============================

if __name__ == "__main__":
    run()
