import webbrowser
import platform
import subprocess
import urllib.parse
from typing import List, Dict, Any
from utils.helpers import info, warn, wait

DEFAULT_PAUSE_SECONDS = 1
STEAM_SELL_URL = "https://steamcommunity.com/market/sellitem"


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
    using the market_hash_name, category, and appid from JSON data.
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

        sell_url = generate_sell_url(item)

        if dry_run:
            info(f"[Dry Run] URL: {sell_url}")
            # Print clickable link for supported terminals
            print(f"\033]8;;{sell_url}\a[Dry Run: {item.get('market_hash_name')} | "
                  f"{item.get('category', 'unknown')} | ${item.get('recommended_price',0):.2f}]\033]8;;\a")
            wait(pause_seconds)
        else:
            info(f"Opening sell page for: {item.get('market_hash_name')}")
            open_url_in_browser(sell_url)
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
    category = item.get("category", "unknown")
    print(f"\n[{index}/{total}] {name} | {category} - ${price:.2f}")


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
    Generate Steam Market sell URL from item.
    """
    name_encoded = urllib.parse.quote(item.get("market_hash_name", "UNKNOWN"))
    appid = item.get("appid")
    contextid = item.get("contextid", "2")
    assetid = item.get("assetid")
    price_cents = int(round(item.get("recommended_price", 0) * 100))

    return (
        f"{STEAM_SELL_URL}"
        f"?appid={appid}"
        f"&contextid={contextid}"
        f"&assetid={assetid}"
        f"&price={price_cents}"
        f"&market_hash_name={name_encoded}"
    )


def open_url_in_browser(url: str) -> None:
    """
    Open a URL in the default browser.
    Uses explorer.exe if running in WSL.
    """
    try:
        import platform
        import subprocess
        if platform.system() == "Linux":
            subprocess.run(["explorer.exe", url.replace("&", "^&")], check=False)
            return
    except Exception:
        pass

    import webbrowser
    webbrowser.open_new_tab(url)
