from auth import session_manager
from inventory import inventory_fetcher
from market import price_fetcher
from filtering import filter_manager
from queue import queue_manager
from workflow import workflow_runner
from utils.helpers import info, warn

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
    # 2. Inventory Retrieval
    # -----------------------------
    raw_inventory = inventory_fetcher.fetch_inventory(session_headers)
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
    # TODO: replace with real user input or config
    categories = None
    min_price = None
    max_price = None
    sort_key = "price"

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

    if not listing_queue:
        warn("Listing queue is empty. Exiting.")
        return
        
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
        
    export_path = "listing_queue.json"
    queue_manager.export_queue(listing_queue, export_path)
    info(f"Queue exported to {export_path}")

    info(f"Queue summary:")
    info(f"  Total items in queue: {len(listing_queue)}")
    info(f"  Items exceeding minimum price or filters applied: {len(filtered_items)}")
    info(f"  Full inventory size: {len(parsed_inventory)}")

    # -----------------------------
    # 6. Assisted Listing Workflow
    # -----------------------------
    workflow_runner.run_assisted_workflow(listing_queue)

    info("All done!")

if __name__ == "__main__":
    run()