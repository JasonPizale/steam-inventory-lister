# Goals:
    # take filtered inventory items
    # generate a listing queue with all info needed for each item
    # include recommended price and listing URL
    # optionally export queue

def build_listing_queue(items):
    # loop over filtered items
    # for each item, generate listing url (steamcommunity.com/market/sellitem)
    # attach lowest_price and optional notes (like volume)
    # return queue (list of dicts or structured objects)
    pass

def calculate_recommended_price(item):
    # decide price based on lowest_price only
    # return numeric value
    pass

def export_queue(queue, filepath=None):
    # optionally save queue to CSV or JSON
    # if no filepath -> just keep in memory
    pass