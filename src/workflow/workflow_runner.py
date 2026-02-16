import webbrowser
import platform
import subprocess
import urllib.parse
from typing import List, Dict, Any
from utils.helpers import info, warn, wait

STEAM_SELL_URL = "https://steamcommunity.com/market/sellitem"
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
    using only the market_hash_name, appid, and recommended price from JSON data.
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
        sell_url = build_sell_url(item)

        if dry_run:
            info(f"[Dry Run] URL: {sell_url}")

            # Print as clickable link in supported terminals
            print(f"\033]8;;{sell_url}\a[Dry Run: {item.get('market_hash_name')}]\033]8;;\a")

            # Attempt to open automatically in browser if possible
            try:
                webbrowser.open_new_tab(sell_url)
            except Exception:
                warn("Unable to automatically open URL in browser. Copy it manually.")

            wait(pause_seconds)
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

def build_sell_url(item: Dict[str, Any]) -> str:
    """
    Build Steam Market Sell Item URL for the item with price pre-filled.
    Format:
    https://steamcommunity.com/market/sellitem/?appid=730&contextid=2&assetid=12345&price=1234
    """
    name_encoded = urllib.parse.quote(item.get("market_hash_name", "UNKNOWN"))
    appid = item.get("appid", 730)
    contextid = item.get("contextid", "2")
    assetid = item.get("assetid")
    price = item.get("recommended_price", 0)

    # Steam price uses cents, multiply by 100 and round
    price_cents = int(round(price * 100))

    return (
        f"{STEAM_SELL_URL}"
        f"?appid={appid}"
        f"&contextid={contextid}"
        f"&assetid={assetid}"
        f"&price={price_cents}"
        f"&market_hash_name={name_encoded}"
    )
