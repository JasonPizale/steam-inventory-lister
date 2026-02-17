import json
import time
from inventory import inventory_fetcher
from market import price_fetcher
from filtering import filter_manager
from utils.helpers import info, warn, prompt_optional_float, prompt_sort_key
from collections import Counter

def run():
    info("Starting Steam Inventory Analyzer")

    # -----------------------------
    # Load JSON
    # -----------------------------
    json_path = input("Enter path to your Steam inventory JSON: ").strip()
    if not json_path:
        warn("No file path provided. Exiting.")
        return

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            raw_inventory = json.load(f)
    except Exception as e:
        warn(f"Failed to load JSON: {e}")
        return

    parsed_inventory = inventory_fetcher.parse_inventory(raw_inventory)
    if not parsed_inventory:
        warn("Inventory is empty after parsing. Exiting.")
        return

    info(f"Inventory loaded: {len(parsed_inventory)} items")

    # -----------------------------
    # Price options
    # -----------------------------
    print("\nPrice Options:")
    print("1) Use recommended prices from JSON (fast, no network)")
    print("2) Fetch live Steam Market prices (requires internet)")
    choice = input("Choice (1 or 2, default 1): ").strip()
    live_fetch = choice == "2"

    print("\nSelect currency:")
    print("1) USD")
    print("2) CAD")
    currency_choice = input("Choice (1 or 2, default 1): ").strip()
    currency_map = {"1": 1, "2": 20}  # 1=USD, 20=CAD
    currency_id = currency_map.get(currency_choice, 1)

    if live_fetch:
        print(f"Fetching live prices in {'CAD' if currency_id==20 else 'USD'}...")
    else:
        print("Using recommended prices from JSON.")

    # -----------------------------
    # Price fetching (throttled + batched)
    # -----------------------------
    price_map = {}

    MIN_DELAY = 1.5        # delay between EACH request
    BATCH_SIZE = 20        # number of items per batch
    BATCH_DELAY = 5        # delay between batches

    marketable_items = [item for item in parsed_inventory if item.get("marketable", True)]
    total_items = len(marketable_items)
    info(f"Preparing to fetch prices for {total_items} marketable items")

    for batch_start in range(0, total_items, BATCH_SIZE):
        batch = marketable_items[batch_start:batch_start + BATCH_SIZE]
        batch_number = (batch_start // BATCH_SIZE) + 1
        info(f"Starting batch {batch_number} ({len(batch)} items)")

        for item in batch:
            name = item["market_hash_name"]
            try:
                if live_fetch:
                    price_info = price_fetcher.fetch_live_price(item, currency=currency_id)
                    price = price_info.get("lowest_price", 0.0)
                else:
                    price = item.get("recommended_price", 0.0)

                price_map[name] = price
                info(f"Fetched price for {name}: {price}")
                time.sleep(MIN_DELAY)
            except Exception as e:
                warn(f"Failed to fetch price for {name}: {e}")
                price_map[name] = item.get("recommended_price", 0.0)

        if batch_start + BATCH_SIZE < total_items:
            info(f"Batch {batch_number} complete. Waiting {BATCH_DELAY}s before next batch...")
            time.sleep(BATCH_DELAY)

    parsed_inventory = price_fetcher.merge_prices_with_inventory(parsed_inventory, price_map)

    # -----------------------------
    # Category counts
    # -----------------------------
    category_counts = Counter(filter_manager.detect_category(item) for item in parsed_inventory if item.get("marketable", True))
    info("Available categories:")
    for index, (category, count) in enumerate(sorted(category_counts.items()), start=1):
        print(f"{index}) {category} ({count})")
    print(f"{len(category_counts)+1}) All")

    category_choice = input("Select category number: ").strip()
    selected_categories = None
    if category_choice.isdigit():
        category_index = int(category_choice)
        categories_list = sorted(category_counts.keys())
        if 1 <= category_index <= len(categories_list):
            selected_categories = [categories_list[category_index - 1]]
        elif category_index == len(categories_list) + 1:
            selected_categories = None

    min_price = prompt_optional_float("Minimum price ($): ")
    max_price = prompt_optional_float("Maximum price ($): ")

    # Force sorting to only price or name
    sort_key = prompt_sort_key(allow_game=False)

    # -----------------------------
    # Filtering
    # -----------------------------
    filtered_items = filter_manager.apply_filters(parsed_inventory, selected_categories, min_price, max_price, sort_key)

    if not filtered_items:
        warn("No items matched filters. Exiting.")
        return

    info(f"Filtered items: {len(filtered_items)}")

    # -----------------------------
    # Display summary
    # -----------------------------
    total_value = sum(item.get("recommended_price", 0) for item in filtered_items)
    print("\n=== Inventory Summary ===")
    print(f"Total items: {len(parsed_inventory)}")
    print(f"Filtered items: {len(filtered_items)}")
    print(f"Total estimated value: ${total_value:.2f}")
    print("\nFiltered Items:")
    for item in filtered_items:
        print(f"{item['market_hash_name']} - ${item.get('recommended_price',0):.2f}")

    # -----------------------------
    # Optional export
    # -----------------------------
    export_input = input("\nExport filtered inventory to JSON? (y/n): ").strip().lower()
    if export_input == "y":
        filepath = input("Enter file path to save (e.g., filtered.json): ").strip()
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(filtered_items, f, indent=2)
            info(f"Filtered inventory exported to {filepath}")
        except Exception as e:
            warn(f"Failed to export JSON: {e}")

    info("Done analyzing inventory!")

if __name__ == "__main__":
    run()
