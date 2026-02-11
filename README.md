# Steam Inventory Lister
A utility that loads and analyzes your Steam inventory from a JSON file, uses provided item prices, and helps you prepare multiple items for sale more efficiently.

# Project Goals
- Make it easier to handle large Steam inventories
- Process item values from JSON input
- Help prepare bulk listings without violating Steam's restrictions
- Reduce repetitive manual actions

# Features
- Load Steam inventory from a JSON file
- Use `recommended_price` from inventory data for each item
- Filter items by category or price range
- Generate a listing queue for user review
- Allow user-controlled confirmation of each listing
- No network requests are required to fetch inventory or prices

# Tech Stack
- Python 3.x
- Standard library for JSON handling and file I/O
- (Optional) CLI enhancements for improved usability
- (Optional) Modular structure for easy extensions

# Inventory JSON Example
The program now accepts a JSON file containing your Steam inventory instead of requiring session cookies.

Example structure of the inventory JSON:

```json
{
  "assets": [
    {
      "appid": 730,
      "classid": "123456789",
      "instanceid": "987654321",
      "amount": 1
    },
    {
      "appid": 730,
      "classid": "987654321",
      "instanceid": "123456789",
      "amount": 2
    }
  ],
  "descriptions": [
    {
      "classid": "123456789",
      "instanceid": "987654321",
      "market_hash_name": "AK-47 | Redline (Field-Tested)",
      "marketable": 1,
      "type": "Rifle",
      "icon_url": "https://steamcdn-a.akamaihd.net/...",
      "tags": [
        {"category": "Weapon", "internal_name": "AK-47"}
      ]
    },
    {
      "classid": "987654321",
      "instanceid": "123456789",
      "market_hash_name": "M4A1-S | Hyper Beast (Minimal Wear)",
      "marketable": 1,
      "type": "Rifle",
      "icon_url": "https://steamcdn-a.akamaihd.net/...",
      "tags": [
        {"category": "Weapon", "internal_name": "M4A1-S"}
      ]
    }
  ]
}