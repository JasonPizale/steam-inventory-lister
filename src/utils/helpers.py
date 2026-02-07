import json
import re
import time
from typing import Any, Dict

# -----------------------------
# Logging Helpers
# -----------------------------

def info(msg: str) -> None:
    print(f"[INFO] {msg}")

def warn(msg: str) -> None:
    print(f"[WARN] {msg}")

def error(msg: str) -> None:
    print(f"[ERROR] {msg}")

# -----------------------------
# JSON Helpers
# -----------------------------

def save_json(path: str, data: Dict[str, Any]) -> None:
    """
    Save dict to a JSON file with pretty indentation
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        error(f"Failed to write JSON file {path}: {e}")

def load_json(path: str) -> Dict[str, Any]:
    """
    Safely load JSON. Returns {} on failure instead of crashing
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        warn(f"JSON file not found ({path}), returning empty dict.")
        return {}
    except Exception as e:
        error(f"Failed to load JSON file {path}: {e}")
        return {}

# -----------------------------
# SteamID Utilities
# -----------------------------

STEAMID_64_REGEX = re.compile(r"^[0-9]{17}$")

def is_valid_steamid(steamid: str) -> bool:
    """
    Returns True if string looks like a valid SteamID64
    """
    return bool(STEAMID_64_REGEX.match(steamid))

# -----------------------------
# Time Helpers
# -----------------------------

def wait(seconds: float) -> None:
    """
    Sleep with a visual countdown (useful for rate limits)
    """ 
    for t in range(int(seconds), 0, -1):
        print(f"  Waiting {t}s...", end="\r")
        time.sleep(1)
    print(" " * 40, end="\r")  # clear line

# -----------------------------
# CLI Output Helpers
# -----------------------------

def colour(text: str, c: str) -> str:
    """
    c = 'red', 'green', 'yellow', 'blue'
    """
    colours = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
    }
    reset = "\033[0m"
    return f"{colours.get(c, '')}{text}{reset}"

def good(msg: str) -> None:
    print(colour(msg, "green"))

def bad(msg: str) -> None:
    print(colour(msg, "red"))

def highlight(msg: str) -> None:
    print(colour(msg, "blue"))

def prompt_optional_float(prompt: str):
    """
    Prompt the user for a float value
    """
    while True:
        value = input(prompt).strip()
        if value == "":
            return None
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number or press Enter to skip.")

def prompt_sort_key(default: str = "price") -> str:
    """
    Prompt the user for sort key
    """
    valid_keys = ["price", "name", "game"]
    value = input(
        f"Sort by (price/name/game) [{default}]: "
    ).strip().lower()

    if value == "":
        return default
    
    if value in valid_keys:
        return value

    print(f"Invalid choice, defaulting to {default}")
    return default