import webbrowser
from typing import List, Dict, Any
from utils.helpers import info, warn, wait

# -----------------------------
# Core Workflow Functions
# -----------------------------

def run_assisted_workflow(queue: List[Dict[str, Any]]) -> None:
    """
    Run through a queue of inventory items, prompting user actions when needed
    """
    total = len(queue)

    for index, item in enumerate(queue, start=1):
        display_progress(index, total, item)

        sell_url = item.get("sell_url")
        if sell_url:
            webbrowser.open_new_tab(sell_url)
        else:
            warn("No sell URL found for item")
            continue
    
        pause_for_confirmation(item)

        info(f"Processed item: {item.get('market_hash_name', 'UNKNOWN')}")

    info("Workflow complete!")

def display_progress(index: int, total: int, item: Dict[str, Any]) -> None:
    """
    Display progress through the workflow
    """
    name = item.get("market_hash_name", "UNKNOWN")
    print(f"[{index}/{total}] Processing: {name}")

def pause_for_confirmation(item: Dict[str, Any], pause_seconds: int = 1) -> None:
    """
    Pause execution to let the user confirm or review the item
    """
    name = item.get("market_hash_name", "UNKNOWN")
    response = input(f"Confirm processing item '{name}'? (y/n) ").strip().lower()
    if response != "y":
        warn(f"Skipping item: {name}")
        wait(pause_seconds)  # Optional short pause before continuing
