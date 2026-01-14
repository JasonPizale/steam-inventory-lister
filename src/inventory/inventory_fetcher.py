# goals:
# 1. retrieve a user's inventory using session headers
# 2. handle pagination properly
# 3. ignore items that aren't marketable
# 4. handle errors and retries gracefully

def fetch_inventory(session_headers):
    # 1. start with start = 0
    # 2. loop until more_items is False
    # 3. for each page: 
        # use _get_page(start, session_headers) to retrieve page
        # pass request through retry_fetch() to handle temp. errors
        # collect all items in amaster list
    # 4. once done, return raw inventory JSON list
    # track total_items_fetched, current_page
    # clear error messages if steam returns invalid JSON or authentication fails
    pass

def _get_page(start, session_headers):
    # build the inventory endpoint URL with start parameter
    # send HTTP request (later)
    # return: page items, more_items flag
    # handle 404 or rate_limiting responses gracefully
    pass

def parse_inventory(raw_inventory):
    # loop through raw items
    # extract important fields: name, app id, class id, marketable, icon url, type
    # skip non-marketable items using is_marketable(item)
    # return clean python list/dict or items
    pass

def is_marketable(item):
    # pure function
    # accepts item object
    # returns True if item is marketable, else False
    # used by parse_inventory() and late by filter_manager
    pass

def retry_fetch(url, headers):
    # handle temporary request failures
    # tries request multiple times (later configurable count)
    # one persistent failure -> raise clean error
    pass
