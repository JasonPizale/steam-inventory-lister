from auth import session_manager
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
    # 1. Authentication
    # -----------------------------
    session_headers = session_manager.load_session_from_user()
    if not session_headers:
        warn("Failed to load session. Exiting.")
        return

    # -----------------------------
    # 1b. SteamID input + guardrail
    # -----------------------------
    steamid = input("Enter your 17-digit SteamID64: ").strip()

    # Guardrail: require numeric SteamID64 for now
    if not steamid.isdigit() or len(steamid) != 17:
        warn("Invalid SteamID. Please enter your 17-digit SteamID64.")
        warn("Example: 7656119XXXXXXXXXX")
        return

    # -----------------------------
    # 2. Inventory Retrieval
    # -----------------------------
    raw_inventory = inventory_fetcher.fetch_inventory(
        steamid=steamid,
        session_headers=session_headers
    )

    if not raw_inventory:
        warn("No inventory data retrieved. Exiting.")
        return

    parsed_inventory = inventory_fetcher.parse_inventory(raw_inventory)
    if not parsed_inventory:
        warn("Inventory is empty after parsing. Exiting.")
        return

    info(f"Inventory loaded: {len(parsed_inventory)} items")

    # -----------------------------
    # 3. Market Price Fetching
    # -----------------------------
    price_map = price_fetcher.build_price_map(parsed_inventory, session_headers)
    parsed_inventory = price_fetcher.merge_prices_with_inventory(parsed_inventory, price_map)

    # -----------------------------
    # 4. Item Filtering
    # -----------------------------
    category_counts = Counter(
        item.get("category", "other") for item in parsed_inventory
    )

    info("Detected categories in inventory:")
    for category, count in sorted(category_counts.items()):
        info(f"  {category}: {count}")

    info("Set optional filters (press Enter to skip):")

    min_price = prompt_optional_float("Minimum price ($): ")
    max_price = prompt_optional_float("Maximum price ($): ")
    sort_key = prompt_sort_key()

    category_input = input(
        "Filter by category (comma-separated, or Enter to skip): "
    ).strip().lower()

    categories = (
        [c.strip() for c in category_input.split(",")]
        if category_input
        else None
    )

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
    # 5. Build Listing Queue
    # -----------------------------
    listing_queue = queue_manager.build_listing_queue(filtered_items)

    if not workflow_runner.show_preflight_summary(listing_queue):
        warn("User cancelled before workflow start.")
        return

    if not listing_queue:
        warn("Listing queue is empty. Exiting.")
        return

    # --- Pre-flight summary ---
    info("Pre-flight summary:")
    info(f"  Inventory items: {len(parsed_inventory)}")
    info(f"  Filtered items: {len(filtered_items)}")
    info(f"  Listing queue: {len(listing_queue)}")

    # --- Dry-run prompt ---
    dry_run_input = input("Run in dry-run mode (no browser tabs)? (y/n): ").strip().lower()
    dry_run = dry_run_input == "y"
    if dry_run:
        warn("Dry run mode enabled - no browser tabs will be opened.")

    # -----------------------------
    # Guardrail: prevent accidental tab explosion
    # ----------------------------- 
    MAX_AUTO_ITEMS = 25
    if len(listing_queue) > MAX_AUTO_ITEMS:
        confirm = input(
            f"You are about to process {len(listing_queue)} items. Continue? (y/n): "
        ).strip().lower()
        if confirm != "y":
            warn("User aborted workflow.")
            return

    # -----------------------------
    # Export queue and display summary
    # -----------------------------
    export_input = input("Export listing queue to JSON? (y/n): ").strip().lower()
    if export_input == "y":
        filepath = input("Enter file path to save queue (e.g., queue.json): ").strip()
        queue_manager.export_queue(listing_queue, filepath)

    total_inventory = len(parsed_inventory)
    total_filtered = len(filtered_items)
    total_queue = len(listing_queue)
    total_estimated_value = sum(
        item.get("recommended_price", 0) for item in listing_queue
    )

    info(f"Summary:")
    info(f"  Total inventory items: {total_inventory}")
    info(f"  Filtered items: {total_filtered}")
    info(f"  Listing queue length: {total_queue}")
    info(f"  Total estimated value: ${total_estimated_value:.2f}")

    # -----------------------------
    # 6. Assisted Listing Workflow
    # -----------------------------
    workflow_runner.run_assisted_workflow(
        listing_queue,
        dry_run=dry_run
    )

    info("All done!")

if __name__ == "__main__":
    run()