import webbrowser
from typing import List, Dict, Any
from utils.helpers import info, warn, wait

DEFAULT_PAUSE_SECONDS = 1

def show_preflight_summary(queue: List[Dict[str, Any]]) -> bool:
    """
    Show a summary of the listing queue and ask the user to confirm before proceeding.
    Returns True if user confirms
    """
    total = len(queue)
    prices = [item["recommended_price"] for item in queue if item.get("recommended_price")]

    print("\n=== Listing Summary ===")
    print(f"Total items: {total}")

    if prices:
        print(f"Lowest price: ${min(prices):.2f}")
        print(f"Highest price: ${max(prices):.2f}")
        print(f"Average price: ${sum(prices)/len(prices):.2f}")
    
    response = input("Proceed with listing? [y/n]: ").strip().lower()
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
    Run through a queue of inventory items, opening the sell page in browser
    and letting the user confirm each listing manually.

    Controls:
    y = open sell page
    n = skip item
    q = quit 
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

        sell_url = item.get("sell_url")
        if not sell_url:
            warn(f"No sell URL found for item: {item.get('market_hash_name')}")
            skipped += 1
            continue

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

def display_progress(index: int, total: int, item: Dict[str, Any]) -> None:
    """
    Display progress through the workflow
    """
    name = item.get("market_hash_name", "UNKNOWN")
    print(f"\n[{index}/{total}] {name}")

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