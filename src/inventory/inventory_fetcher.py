from typing import Dict, Any, List

# -----------------------------
# Parsing
# -----------------------------
def parse_inventory(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Merge assets + descriptions into item objects from JSON inventory file.
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
        merged.append(item)

    return merged

def is_marketable(desc: Dict[str, Any]) -> bool:
    """Steam uses 'marketable: 1' to denote marketable items."""
    return desc.get("marketable", 0) == 1

# -----------------------------
# Direct execution guard
# -----------------------------
if __name__ == "__main__":
    print("This module is now for parsing JSON inventory files only.")
