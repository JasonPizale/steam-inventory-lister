import webbrowser
from typing import List, Dict, Any
from utils.helpers import info, warn, wait

DEFAULT_PAUSE_SECONDS = 1

# -----------------------------
# Preflight Summary
# -----------------------------
def show_preflight_summary(queue: List[Dict[str, Any]]) -> bool:
    """
    Show a summary of the listing queue and ask the user to confirm before proceeding.
    Returns True if user confirms
    """
    total = len(queue)
    prices = [item.get("recommended_price", 0) for item in queue if item.get("recommended_price")]

    print("\n=== Listing Summary ===")
    print(f"Total items: {total}")

    if prices:
        print(f"Lowest price: ${min(prices):.2f}")
        print(f"Highest price: ${max(prices):.2f}")
        print(f"Average price: ${sum(prices)/len(prices):.2f}")
    
    response = input("Proceed with assisted workflow? [y/n]: ").strip().lower()
    return response == "y"

# -----------------------------
# Core Workflow Functions
# -----------------------------
def run_assisted_workflow(
        queue: List[Dict[str, Any]],
        dry_run: bool = False,
        pause_seconds: int = DEFAULT_PAUSE_SECONDS
) -> None:
    """
    Walk through each inventory item in the queue, optionally opening the Steam Market sell page
    using only the market_hash_name and appid from JSON data.
    """

    total = len(queue)
    opened = 0
    skipped = 0

    info(f"Starting assisted workflow ({total} items)")
    if dry_run:
        warn("Dry run mode enabled - no browser tabs will be opened.")

    for index, item in enumerate(queue, start=1):
        display_progress(index, total, item)
        user_action = prompt_user(item)
        if user_action == "q":
            warn("Workflow aborted by user")
            break
        if user_action == "n":
            skipped += 1
            continue

        # Generate Steam Market sell URL from JSON data
        sell_url = generate_sell_url(item)
        if dry_run:
            info(f"[Dry Run] Would open: {sell_url}")
        else:
            info(f"Opening sell page for: {item.get('market_hash_name')}")
            webbrowser.open_new_tab(sell_url)
            wait(pause_seconds)

        opened += 1

    info("Workflow complete")
    info(f"Opened: {opened}")
    info(f"Skipped: {skipped}")
    info(f"Remaining: {total - opened - skipped}")

# -----------------------------
# Helpers
# -----------------------------
def display_progress(index: int, total: int, item: Dict[str, Any]) -> None:
    """
    Display progress through the workflow
    """
    name = item.get("market_hash_name", "UNKNOWN")
    price = item.get("recommended_price", 0.0)
    print(f"\n[{index}/{total}] {name} - ${price:.2f}")

def prompt_user(item: Dict[str, Any]) -> str:
    """
    Prompt the user for action on the current item.
    Returns 'y' (open), 'n' (skip), or 'q' (quit).
    """
    name = item.get("market_hash_name", "UNKNOWN")

    while True:
        choice = input(
            f"Process '{name}'? [y = open, n = skip, q = quit]: "
        ).strip().lower()

        if choice in ("y", "n", "q"):
            return choice
        
        warn("Invalid input. Please enter 'y', 'n', or 'q'.")

def generate_sell_url(item: Dict[str, Any]) -> str:
    """
    Generate a Steam Market sell URL from market_hash_name and appid.
    Format: https://steamcommunity.com/market/listings/{appid}/{market_hash_name}
    """
    appid = item.get("appid", 730)
    name = item.get("market_hash_name", "UNKNOWN").replace(" ", "%20")
    return f"https://steamcommunity.com/market/listings/{appid}/{name}"
