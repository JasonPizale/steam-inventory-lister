# Phase 1 -- Setup & Research
  GOALS: get environment ready, understand Steam data formats
  - set up project folder structure
  - research Steam inventory & market endpoints
  - remove live authentication (cookies/session)
  - document JSON inventory structure and API quirks
### MILESTONE: Environment ready and JSON format understood.

# Phase 2 -- Inventory Retrieval Module
  GOALS: load user inventory from JSON
  - prompt user to provide exported inventory JSON file
  - parse JSON into structured inventory objects
  - handle empty inventories and missing fields
  - include key fields: name, app ID, class ID, marketability, icon, type, optional recommended price
### MILESTONE: Inventory is fully loadable and readable from JSON.

# Phase 3 -- Market Price Handling Module
  GOALS: handle item pricing
  - use `recommended_price` from JSON
  - live Steam market price fetching is disabled
  - placeholder logic in price_fetcher retained for offline testing
### MILESTONE: Items can be processed with pricing information from JSON.

# Phase 4 -- Filtering & Selection Logic
  GOALS: let the user choose what to list
  - filter by category (game type, trading cards, etc.)
  - filter by price range (using JSON `recommended_price`)
  - sort items by value, name, or game
  - display filtered list in a clean format
### MILESTONE: User can create a "listable items" set from JSON inventory.

# Phase 5 -- Listing Preparation Module
  GOALS: prepare data needed to create listings
  - generate listing queue from filtered inventory
  - export queue to JSON for later use
  - listing URLs can still be generated if needed
### MILESTONE: Listing queue is fully structured and ready for assisted workflow.

# Phase 6 -- Assisted Listing Workflow
  GOALS: guide the user to create listings manually
  - display queue with progress info (e.g., "item 12/23")
  - let user manually confirm each listing
  - automatic browser tab opening removed
### MILESTONE: User can bulk-list items with minimal effort, using JSON input.

# Phase 7 -- Polish, Cleanup & Stretch Goals
  OPTIONAL IMPROVEMENTS:
  - CLI enhancements (menus, colors)
  - CSV export
  - summary stats
  - async speedup and live Steam integration postponed
  - improve error messages and UX for JSON workflow
  - clean up codebase and documentation

# Project Completion Criteria
  - inventory can be loaded from JSON
  - items can be filtered and sorted
  - a listing queue can be created
  - user can review queue and manually confirm listings
  - program works without requiring Steam authentication