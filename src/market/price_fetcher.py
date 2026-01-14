# goals:
# 1. for each marketable item in inventory, fetch its price
# 2. handle steam rate limits gracefully
# 3. parse lowest price, volume, optionally price graphs
# 4. merge price info back into inventory
# 5. be robust to missing or malformed data

def get_price_for_item(item, session_headers):
    # build market url using build_price_url(item)
    # call fetch_price(url, session_headers) to get JSON data
    # return parsed price data (lowest_price, volume) (price graph optional)
    pass

def build_price_url(item):
    # construct steam market price url
    # properly url-encode item names (market_hash_name)
    # include app id and any required parameters
    pass

def fetch_price(url, session_headers):
    # use retry_fetch() to make request resilient
    # parse JSON response
    # detect rate-limits -> call handle_rate_limit() if necessary
    # if price missing, return fallback values
    pass

def handle_rate_limit(response):
    # detect steam rate-limit response (e.g., HTTP 429 or empty/invalid JSON)
    # pause/sleep for a few seconds before retrying
    pass

def merge_prices_with_inventory(inventory, price_map):
    # attach lowest_price, volume, etc., to each inventory item
    # skip items without price data
    pass

def build_price_map(inventory, session_headers):
    # iterate over unique items to avoid redundant requests
    # for each item call get_price_for_item(item, session_headers)
    # store results in a dict keyed by (app_id, class_id) or market_hash_name
    pass
