# Phase 1 -- Setup & Research
  GOALS: get environment ready, understand steam endpoints
  - set up project folder structure
  - research steam inventory & market endpoints
  - identify authentication method (session cookies)
  - document any API quirks or rate limits
  - Add notes to research.md

# Phase 2 -- Inventory Retrieval Module
  GOALS: retrieve and format user inventory
  - implement authentication input (cookies/session ID)
  - send inventory request
  - handle pagination
  - pause item field (name, app ID, class ID, marketability, icon, type)
  - handle errors, empty inventories, and non-marketable items
  - output clean structured inventory data 
### MILESTONE: Inventory is fully retrievable and readable.

# Phase 3 -- Market Price Fetching Module
  GOALS: fetch market price for each item
  - query steam market price overview endpoint
  - Parse the lowest price and volume
  - handle rate limiting
  - add fallback behaviour for failed requests
  - cache responses (optional)
  - combine price data with inventory items
### MILESTONE: Every marketable item now has pricing data attached.

# Phase 4 -- Filtering & Selection Logic
  GOALS: let the user choose what to list
  - filter by category (game type, trading cards, etc.)
  - filter by price range
  - sort items by value or game
  - display filtered list in a clean format
### MILESTONE: User can create a "listable items" set.

# Phase 5 -- Listing Preparation Module
  GOALS: prepare data needed to create listings
  - generate recommended price
  - format a "listing queue"
  - generate listing URLs for steamcommunity.com/market/sellitem
  - store queue in memory or export (optional)
### MILESTONE: Listing queue is fully structured and ready.

# Phase 6 -- assisted listing workflow
  GOALS: execute the listing queue and guide the user.
  - open listing URLs sequentially
  - optionally add delays
  - display progress (e.g., "item 12/23")
  - let user confirm each listing manually in browser
### MILESTONE: User can bulk-list items with minimal manual clicking.

# Phase 7 -- polish, cleanup & stretch goals
  OPTIONAL IMPROVEMENTS:
  - add CLI enhancements (menus, colours)
  - add CSV export
  - add summary stats
  - add optional async speedup
  - improve error messages and UX
  - clean up codebase and documentation

# Project Completion Criteria
  - inventory can be retrieved
  - prices can be fetched
  - items can be filtered
  - a listing queue can be created
  - listing URLs can be opened sequentially
  - user can quickly confirm listings manually

