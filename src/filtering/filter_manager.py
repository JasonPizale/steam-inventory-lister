# goals
# 1. let the user filter inventory by categories
# 2. let user filter by price range (min/max)
# 3. optionally, sort items (by price, name, game)
# 4. return a clean list ready for listing queue

def filter_by_category(items, categories):
    # loop through items
    # keep only items whose type is in allowed categories
    # skip items that aren't marketable (is_marketable(item))
    pass

def filter_by_price(items, min_price, max_price):
    # loop through items
    # keep only items where lowest_price is within the range
    # skip items without a price
    pass

def sort_items(items, key, descending=False):
    # sorting function
    # sort by lowest_price, name or game
    pass

def apply_filters(items, categories, min_price, max_price, sort_key=None):
    # sequentiall call: filter_by_category, filter_by_price, sort_items
    # return final filtered list for queue building
    pass

