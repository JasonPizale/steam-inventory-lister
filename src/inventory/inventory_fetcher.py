import requests
import time
from typing import Dict, Any, List

STEAM_INVENTORY_URL = (
    "https://steamcommunity.com/inventory/{steamid}/{app_id}/{context_id}"
    "?l=english&count=5000&start={start}"
)

class InventoryFetchError(Exception):
    """Custom error for inventory fetch failures."""
    pass

# -----------------------------
# Public API
# -----------------------------
def fetch_inventory(
    steamid: str,
    session_data: Dict[str, Dict[str, str]],
    app_id: int = 730,
    context_id: int = 2,
    max_retries: int = 3
) -> Dict[str, Any]:
    """
    Fetch entire inventory across paginated pages.
    """
    print("[fetch_inventory] Starting fetch...")

    combined = {"assets": [], "descriptions": []}
    start = 0
    page_num = 1

    while True:
        print(f"[fetch_inventory] Fetching page {page_num}")

        page = retry_fetch(
            lambda: _get_page(
                steamid=steamid,
                session_data=session_data,
                app_id=app_id,
                context_id=context_id,
                start=start
            ),
            max_retries=max_retries
        )

        combined["assets"].extend(page.get("assets", []))
        combined["descriptions"].extend(page.get("descriptions", []))

        if page.get("more_items"):
            start = page.get("last_assetid", 0)
            page_num += 1
        else:
            break

    print("[fetch_inventory] Done.")
    return combined

# -----------------------------
# Single page fetch
# -----------------------------
def _get_page(
    steamid: str,
    session_data: Dict[str, Dict[str, str]],
    app_id: int,
    context_id: int,
    start: int
) -> Dict[str, Any]:
    """Fetch a single inventory page from Steam."""
    url = STEAM_INVENTORY_URL.format(
        steamid=steamid,
        app_id=app_id,
        context_id=context_id,
        start=start
    )

    headers = session_data.get("headers", {})
    cookies = session_data.get("cookies", {})

    try:
        resp = requests.get(url, headers=headers, cookies=cookies, timeout=15)
    except Exception as e:
        raise InventoryFetchError(f"Network error: {e}")

    if resp.status_code != 200:
        raise InventoryFetchError(f"Steam returned HTTP {resp.status_code}")

    try:
        data = resp.json()
    except ValueError:
        raise InventoryFetchError("Steam returned non-JSON response")

    if data.get("success") != 1:
        raise InventoryFetchError("Steam inventory API indicated failure")

    return data

# -----------------------------
# Retry wrapper
# -----------------------------
def retry_fetch(func, max_retries: int = 3, delay: float = 1.0):
    """Retry wrapper used for Steam API calls."""
    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except InventoryFetchError as e:
            print(f"[retry_fetch] Attempt {attempt}/{max_retries} failed: {e}")
            if attempt == max_retries:
                raise
            time.sleep(delay)

# -----------------------------
# Parsing
# -----------------------------
def parse_inventory(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Merge assets + descriptions into item objects.
    """
    assets = raw.get("assets", [])
    descriptions = raw.get("descriptions", [])

    desc_map = {}
    for d in descriptions:
        key = (d.get("classid"), d.get("instanceid"))
        desc_map[key] = d

    merged = []
    for asset in assets:
        key = (asset.get("classid"), asset.get("instanceid"))
        desc = desc_map.get(key, {})

        item = {**asset, **desc}
        item["marketable"] = is_marketable(desc)
        merged.append(item)

    return merged

def is_marketable(desc: Dict[str, Any]) -> bool:
    """Steam uses 'marketable: 1' to denote marketable items."""
    return desc.get("marketable", 0) == 1

# -----------------------------
# Direct execution guard
# -----------------------------
if __name__ == "__main__":
    print("This module should be imported, not executed directly.")
