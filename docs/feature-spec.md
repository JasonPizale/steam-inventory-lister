# Overview 
- a tool that retrieves a user's Steam inventory, analyzes the items, fetches market prices, and prepares items for listing on the Steam Market.
- The tool assists with all steps up to the final listing confirmation, which must still be performed by the user.

# In-Scope Features
1. Inventory Retrieval
   - retrieve the user's full Steam inventory
   - handle inventory pagination
   - identify item name, app ID, class ID, marketability, icon, type
2. Market Price Fetching
   - retrieve the lowest listing price for each marketable item and the graph
   - handle api rate limits and errors
3. Item Filtering
   - filter by categories
   - filter by price range
4. Listing Preparation
   - create a queue for selected items
5. Assisted Listing Workflow
   - sequentially open browser tabs/pages for each item
   - allow user to confirm each sale manually
6. Requirements
   - Functional
       - must authenticate the user using cookies or session tokens
       - must fetch inventory reliably with clear errors
       - must fetch market data and display it
       - must allow user-defined filters
       - must generate a "listing prep queue"
       - must allow user-controlled execution of the queue
    - Non-Functional
       - must avoid violating Steam's TOS
       - must use clear logging or user feedback
       - must handle network failures gracefully
       - should provide clean, readable output (CLI or minimal UI)
       - code should be modular and maintainable
7. Data Flow Overview
   1. user authenticates -> provides session cookies
   2. program fetches inventory
   3. program fetches market prices
   4. user filters items
   5. program generates a list of items to list
   6. program opens listing URLs in order
   7. user confirms listings
   8. program moves to next item 
  
