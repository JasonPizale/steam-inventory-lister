import requests
from typing import Dict, Tuple

# -----------------------------
# Public API
# -----------------------------
def load_session_from_user() -> Dict[str, str]:
    """
    Ask the user to paste Steam cookies and return a headers dict
    ready for requests.get.
    """
    print("\n=== Steam Session Setup ===")
    print("Paste your Steam cookies (from browser) below.")
    print("Example: steamLoginSecure=...; sessionid=...; browserid=...\n")

    raw = input("Cookies: ").strip()
    if not raw:
        raise ValueError("No cookies input provided.")

    cookies_dict = _parse_cookies(raw)
    if not cookies_dict:
        raise ValueError("Failed to parse cookies from input.")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://steamcommunity.com/"
    }

    # Return headers **and cookies separately** for proper requests usage
    session_data = {
        "headers": headers,
        "cookies": cookies_dict
    }

    print("✅ Cookies loaded successfully.\n")
    return session_data

# -----------------------------
# Session Validation
# -----------------------------
def validate_session(session_data: Dict[str, Dict[str, str]]) -> bool:
    """
    Test if the headers/cookies are valid by fetching Steam profile page.
    """
    headers = session_data.get("headers", {})
    cookies = session_data.get("cookies", {})
    test_url = "https://steamcommunity.com/my/"

    try:
        response = requests.get(test_url, headers=headers, cookies=cookies, timeout=10)
    except Exception:
        print("Failed to connect to Steam for session validation.")
        return False

    if response.status_code != 200:
        print(f"Unexpected response code: {response.status_code}")
        return False

    # TODO: Add proper HTML parsing to verify login
    print("✅ Session appears valid (page loaded).")
    return True

# -----------------------------
# Helper: Parse raw cookie string
# -----------------------------
def _parse_cookies(cookie_string: str) -> Dict[str, str]:
    """
    Convert a raw "k=v; k2=v2" string into a dict.
    """
    cookies = {}
    for pair in cookie_string.split(";"):
        if "=" not in pair:
            continue
        key, value = pair.strip().split("=", 1)
        cookies[key.strip()] = value.strip()
    return cookies

# -----------------------------
# Direct execution guard
# -----------------------------
if __name__ == "__main__":
    session_data = load_session_from_user()
    if validate_session(session_data):
        print("You can now fetch inventory safely!")
    else:
        print("Session invalid. Check your cookies and try again.")
