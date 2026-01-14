# Goals:
# sequentially process the listing queue
# open each item's listing url in browser
# pause for manual confirmation before moving to next item

def run_assisted_workflow(queue):
    # loop through queue
    # for each item:
        # open browser to listing page
        # call pause_for_confirmation(item)
        # display progress ("item 5/20")
    pass

def display_progress(index, total):
    # simple helper to show CLI progress
    pass

def pause_for_confirmation(item):
    # wait for user to confirm they listed the item before continuing
    pass


