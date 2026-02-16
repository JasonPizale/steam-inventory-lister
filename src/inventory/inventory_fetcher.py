from typing import Dict, Any, List

# -----------------------------
# Parsing
# -----------------------------
def parse_inventory(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Merge assets + descriptions into item objects from JSON inventory file.
    Attach normalized category for better UX filtering.
    """
    assets = raw.get("assets", [])
    descriptions = raw.get("descriptions", [])

    desc_map = {}
    for d in descriptions:
        key = (d.get("classid"), d.get("instanceid"))
        desc_map[key] = d

    merged = []
    for asset in assets:
        key = (asset.get("classid"), asset.get("instanceid"))
        desc = desc_map.get(key, {})

        item = {**asset, **desc}
        item["marketable"] = is_marketable(desc)

        # 🔥 Add normalized category
        item["category"] = categorize_item(desc)

        merged.append(item)

    return merged


def is_marketable(desc: Dict[str, Any]) -> bool:
    """Steam uses 'marketable: 1' to denote marketable items."""
    return desc.get("marketable", 0) == 1


# -----------------------------
# Category Normalization
# -----------------------------
def categorize_item(desc: Dict[str, Any]) -> str:
    """
    Convert Steam 'type' field into logical sell categories.
    """
    type_name = desc.get("type", "").lower()

    # Weapon skins
    if any(word in type_name for word in [
        "rifle", "sniper", "pistol", "smg", "shotgun"
    ]):
        return "Weapon Skin"

    # Stickers
    if "sticker" in type_name:
        return "Sticker"

    # Cases / containers
    if "container" in type_name or "case" in type_name:
        return "Case"

    # Keys
    if "key" in type_name:
        return "Key"

    # Gloves
    if "glove" in type_name:
        return "Gloves"

    # Knives
    if "knife" in type_name:
        return "Knife"

    return "Other"


# -----------------------------
# Direct execution guard
# -----------------------------
if __name__ == "__main__":
    print("This module is now for parsing JSON inventory files only.")
