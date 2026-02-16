import json
from inventory import inventory_fetcher
from market import price_fetcher
from filtering import filter_manager
from queue_manager_pkg import queue_manager
from workflow import workflow_runner
from utils.helpers import info, warn, prompt_optional_float, prompt_sort_key
from collections import Counter

def run():
    info("Starting Steam Market Assistant")

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
    # Robust Price Fetching
    # -----------------------------
    price_map = {}
    MIN_DELAY = 1.5
    for item in parsed_inventory:
        if not item.get("marketable", True):
            continue
        try:
            price_info = price_fetcher.fetch_live_price(item, currency=currency_id)
            price_map[item["market_hash_name"]] = price_info.get("lowest_price", 0)
            info(f"Fetched price for {item['market_hash_name']}: {price_map[item['market_hash_name']]}")
            time.sleep(MIN_DELAY)
        except Exception as e:
            warn(f"Failed to fetch price for {item.get('market_hash_name')}: {e}")
            price_map[item["market_hash_name"]] = 0.0

    parsed_inventory = price_fetcher.merge_prices_with_inventory(parsed_inventory, price_map)

    # -----------------------------
    # Item Filtering
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
    sort_key = prompt_sort_key()

    filtered_items = filter_manager.apply_filters(parsed_inventory, selected_categories, min_price, max_price, sort_key)

    if not filtered_items:
        warn("No items matched filters. Exiting.")
        return

    info(f"Filtered items: {len(filtered_items)}")

    # -----------------------------
    # Build Listing Queue
    # -----------------------------
    listing_queue = queue_manager.build_listing_queue(filtered_items)

    if not listing_queue:
       warn("Listing queue is empty. Exiting.")
       return

    if not workflow_runner.show_preflight_summary(listing_queue):
        warn("User cancelled before workflow start.")
        return

    dry_run_input = input("Run in dry-run mode (no browser tabs)? (y/n): ").strip().lower()
    dry_run = dry_run_input == "y"
    if dry_run:
        warn("Dry run mode enabled - no browser tabs will be opened.")

    MAX_AUTO_ITEMS = 25
    if len(listing_queue) > MAX_AUTO_ITEMS:
        confirm = input(f"You are about to process {len(listing_queue)} items. Continue? (y/n): ").strip().lower()
        if confirm != "y":
            warn("User aborted workflow.")
            return

    export_input = input("Export listing queue to JSON? (y/n): ").strip().lower()
    if export_input == "y":
        filepath = input("Enter file path to save queue (e.g., queue.json): ").strip()
        queue_manager.export_queue(listing_queue, filepath)

    total_inventory = len(parsed_inventory)
    total_filtered = len(filtered_items)
    total_queue = len(listing_queue)
    total_estimated_value = sum(item.get("recommended_price", 0) for item in listing_queue)

    info(f"Summary:")
    info(f"  Total inventory items: {total_inventory}")
    info(f"  Filtered items: {total_filtered}")
    info(f"  Listing queue length: {total_queue}")
    info(f"  Total estimated value: ${total_estimated_value:.2f}")

    workflow_runner.run_assisted_workflow(listing_queue, dry_run=dry_run)

    info("All done!")

if __name__ == "__main__":
    run()
