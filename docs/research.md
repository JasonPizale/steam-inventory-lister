# Steam Inventory Endpoint
  - base URL format
  - required parameters
  - pagination behaviour (start, count)
  - notes on marketable vs. non-marketable items
  - sample request URL (no cookies)

# Steam Market Price Overview Endpoint
  - base URL format
  - required parameters
  - response fields: lowest_price and volume
  - rate limit notes
  - known quirks (e.g. sometimes returns empty data)

# Authentication
  - required cookies (e.g. steamLoginSecure, sessionid)
  - how user will supply them
  - limitations (cannot  bypass steam guard, cannot auto-confirm listings)

# Browser -> Steam Workflow Notes
  - how listing URLs behaves
  - how steam confirms listings
  - what parts cannot be automated
  - any CAPTCHAs or blockers

# what still needs investigation
  - price history graph endpoint
  - Async request behaviour
  - inventory inconsistencies
  - steam downtime/maintenance behaviour
