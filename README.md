# Steam Inventory Analyzer

![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![Requests](https://img.shields.io/badge/requests-installed-green)

## Pivoted Project
Originally a Steam Market listing tool, this project now focuses on **analyzing your Steam inventory**, sorting items by category, and calculating **total estimated value**.

---

## Features ✅
- Load your Steam inventory JSON.
- Fetch or use pre-existing recommended prices for items.
- Filter items by **category**, **price range**, and **name**.
- Sort items by **price** or **name**.
- Summarize **total inventory value** and filtered item counts.
- Designed for **speed and usability with large inventories**.

---

## Getting Started 🚀

### 1. Clone the repository

### 2. Prepare your inventory JSON
- Export your Steam inventory via Steam Web or from a local backup.

### 3. Run the analyzer
- python3 main.py

### 4. Follow the prompts
- Choose whether to fetch live prices or use recommended JSON prices.
- Select currency (USD or CAD).
- Pick categories to filter (or choose "All").
- Set optional minimum/maximum price filters.
- View summarized results in the terminal.

### Notes ⚠️
- Live price fetching may trigger Steam rate limits.
- For large inventories, use recommended JSON prices for faster runs.
- This project no longer lists items on the Steam Market.
- All workflow/browser automation features have been removed.

### Project Structure 📁
- main.py                   ← Main script for loading, filtering, sorting, and summarizing inventory
- inventory/                ← Inventory parsing utilities
- market/                   ← Price fetching functions
- filtering/                ← Item category detection and filter functions
- utils/helpers.py          ← Logging, input prompts, and helper functions

### Usage Example 💻
  Run the script:
  
    - python3 main.py
    
  Example prompts:
  
    Select price option: 2
    Select currency: 1 (USD)
    Available categories:
        1) case
        2) other
        3) weapon skin
        4) All
      Select category number: 3
      Minimum price ($): 0.05
      Maximum price ($): 500
      Sort by (price/name) [price]: price
    
  Sample output:
  
    Filtered items: 18
    Total inventory items: 90
    Listing queue length: 18
    Total estimated value: $345.12
