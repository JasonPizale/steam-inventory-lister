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

    # -----------------------------
    # 1. Load Inventory from JSON
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
    # 2. Market Price Fetching (optional live prices)
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

    price_map = price_fetcher.build_price_map(
        parsed_inventory,
        live_fetch=live_fetch,
        currency=currency_id,
        delay=0.5
    )

    parsed_inventory = price_fetcher.merge_prices_with_inventory(parsed_inventory, price_map)

    # -----------------------------
    # 3. Item Filtering
    # -----------------------------
    category_counts = Counter(item.get("type", "other") for item in parsed_inventory)

    info("Detected categories in inventory:")
    for category, count in sorted(category_counts.items()):
        info(f"  {category}: {count}")

    info("Set optional filters (press Enter to skip):")
    min_price = prompt_optional_float("Minimum price ($): ")
    max_price = prompt_optional_float("Maximum price ($): ")
    sort_key = prompt_sort_key()

    category_input = input("Filter by category (comma-separated, or Enter to skip): ").strip().lower()
    categories = [c.strip() for c in category_input.split(",")] if category_input else None

    filtered_items = filter_manager.apply_filters(
        parsed_inventory,
        categories,
        min_price,
        max_price,
        sort_key
    )

    if not filtered_items:
        warn("No items matched filters. Exiting.")
        return

    info(f"Filtered items: {len(filtered_items)}")

    # -----------------------------
    # 4. Build Listing Queue & Pre-flight
    # -----------------------------
    listing_queue = queue_manager.build_listing_queue(filtered_items)

    if not listing_queue:
       warn("Listing queue is empty. Exiting.")
       return

    # Show summary and ask for confirmation
    if not workflow_runner.show_preflight_summary(listing_queue):
        warn("User cancelled before workflow start.")
        return

    # Dry-run prompt
    dry_run_input = input("Run in dry-run mode (no browser tabs)? (y/n): ").strip().lower()
    dry_run = dry_run_input == "y"
    if dry_run:
        warn("Dry run mode enabled - no browser tabs will be opened.")

    # Guardrail to prevent accidental tab explosion
    MAX_AUTO_ITEMS = 25
    if len(listing_queue) > MAX_AUTO_ITEMS:
        confirm = input(
            f"You are about to process {len(listing_queue)} items. Continue? (y/n): "
        ).strip().lower()
        if confirm != "y":
            warn("User aborted workflow.")
            return

    # Optional export of queue
    export_input = input("Export listing queue to JSON? (y/n): ").strip().lower()
    if export_input == "y":
        filepath = input("Enter file path to save queue (e.g., queue.json): ").strip()
        queue_manager.export_queue(listing_queue, filepath)

    # Display quick summary
    total_inventory = len(parsed_inventory)
    total_filtered = len(filtered_items)
    total_queue = len(listing_queue)
    total_estimated_value = sum(item.get("recommended_price", 0) for item in listing_queue)

    info(f"Summary:")
    info(f"  Total inventory items: {total_inventory}")
    info(f"  Filtered items: {total_filtered}")
    info(f"  Listing queue length: {total_queue}")
    info(f"  Total estimated value: ${total_estimated_value:.2f}")

    # -----------------------------
    # 5. Assisted Listing Workflow
    # -----------------------------
    workflow_runner.run_assisted_workflow(listing_queue, dry_run=dry_run)

    info("All done!")

if __name__ == "__main__":
    run()
