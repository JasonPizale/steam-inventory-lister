import requests

def load_session_from_user():
    print("\n=== Steam Session Setup ===")
    print("Paste your steam cookies (as copied from browser) below:")
    print("Example: steamLoginSecure=...; sessionid=...; browserid=...\n")

    raw = input("Cookies: ").strip()

    if not raw:
        raise ValueError("No cookies input provided.")
   
    cookies = _parse_cookies(raw) # parse the cookies directly

    if not cookies:
        raise ValueError("Failed to parse cookies from input.")
    
    session_data = {
        'cookies': cookies,
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/91.0.4472.124 Safari/537.36"                
    }

    print("Cookies loaded successfully.\n")
    return session_data

def validate_session(session_data):
    headers = get_session_headers(session_data)
    test_url = "https://steamcommunity.com/my/"

    try:
        response = requests.get(test_url, headers=headers)
    except Exception:
        print("Failed to connect to Steam for session validation.")
        return False
    
    if response.status_code != 200:
        print(f"Unexpected response code: {response.status_code}")
        return False

    # debug print for developers
    print("\n--- Response debug ---")
    print("Status code:", response.status_code)
    print("First 500 chars of page:\n", response.text[:500])
    print("--- End debug ---\n")

    # Placeholder logic: update later to detect login state reliably
    # For now, assume cookies are valid if page loads
    session_valid = True  # TODO: implement proper HTML/session check

    if session_valid:
        print("Session is valid.")
        return True
    else:
        print("Session is invalid.")
        return False

def get_session_headers(session_data):
    cookies = session_data.get("cookies", {})
    user_agent = session_data.get("user_agent","")

    cookie_string = "; ".join(f"{k}={v}" for k, v in cookies.items())

    headers = {
        "User-Agent": user_agent,
        "Cookie": cookie_string,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "https://steamcommunity.com/"
    }
    return headers

def _parse_cookies(cookie_string):
    cookie_string = cookie_string.strip()

    cookies = {}

    pairs = cookie_string.split(";")

    for pair in pairs:
        pair = pair.strip()
        if "=" not in pair:
            continue
        key, value = pair.split("=", 1)
        cookies[key.strip()] = value.strip()
    return cookies

# testing
if __name__ == "__main__":
    session_data = load_session_from_user()
    
    valid = validate_session(session_data)
    
    if valid:
        print("\n✅ Session is valid! You can continue with inventory fetching.")
    else:
        print("\n❌ Session is invalid. Check your cookies and try again.")