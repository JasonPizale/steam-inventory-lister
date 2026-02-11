# Overview 
- a tool that loads a user's Steam inventory from a JSON file, analyzes the items, optionally uses provided recommended prices, and prepares items for listing on the Steam Market.
- The tool assists with all steps up to the final listing confirmation, which must still be performed by the user.

# In-Scope Features
1. Inventory Loading
   - user provides a JSON file containing their inventory
   - parse JSON into structured inventory objects
   - identify item name, app ID, class ID, marketability, icon, type, recommended price
2. Market Price Handling
   - use `recommended_price` from JSON for item pricing
   - live Steam market price fetching is disabled
   - placeholder logic remains for testing or offline use
3. Item Filtering
   - filter by categories
   - filter by price range (using JSON prices)
4. Listing Preparation
   - create a queue for selected items
   - optionally export the queue to JSON for later use
5. Assisted Listing Workflow
   - display the listing queue with progress info
   - allow user to confirm each listing manually
   - automatic browser tab opening removed
6. Requirements
   - Functional
       - must load inventory reliably from JSON with clear errors
       - must process item pricing using JSON `recommended_price`
       - must allow user-defined filters
       - must generate a "listing prep queue"
       - must allow user-controlled review and execution of the queue
    - Non-Functional
       - must use clear logging or user feedback
       - should provide clean, readable output (CLI)
       - code should be modular and maintainable
       - network connectivity is no longer required for inventory processing
7. Data Flow Overview
   1. user provides JSON inventory file
   2. program loads inventory from JSON
   3. program processes item pricing from JSON
   4. user filters items
   5. program generates a list of items to list
   6. user reviews listing queue
   7. user confirms listings manually
   8. program moves to next item