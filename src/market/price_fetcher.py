import requests
import time
from utils.helpers import info, warn
import urllib.parse

def build_price_map(items, live_fetch=False, currency=1, delay=0.5):
    price_map = {}
    for item in items:
        try:
            name = item.get("market_hash_name")
            appid = item.get("appid")
            if not live_fetch:
                price_map[name] = item.get("recommended_price", 0)
                continue

            url_name = urllib.parse.quote_plus(name)
            url = (
                f"https://steamcommunity.com/market/priceoverview/"
                f"?currency={currency}&appid={appid}&market_hash_name={url_name}"
            )

            response = requests.get(url)
            data = response.json()
            lowest = data.get("lowest_price")
            if lowest:
                # Strip $/€ etc., convert to float
                price_float = float("".join(c for c in lowest if c.isdigit() or c=='.'))
                price_map[name] = price_float
                info(f"Fetched live price for {name}: {price_float}")
            else:
                price_map[name] = 0.0
                warn(f"No price available for {name}")

        except Exception as e:
            price_map[name] = 0.0
            warn(f"Failed to fetch price for {name}: {e}")

        time.sleep(delay)

    return price_map

def merge_prices_with_inventory(items, price_map):
    for item in items:
        name = item.get("market_hash_name")
        if name in price_map:
            item["recommended_price"] = price_map[name]
    return items
