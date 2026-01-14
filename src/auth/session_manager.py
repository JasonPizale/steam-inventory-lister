# Goals:
# 1. let the user provide their steam session cookie(s)
# 2. store session info in memory for other modules to use
# 3. optionally validate the session lightly
# 4. provide a simple interface for other modules to get headers

def load_session_from_user():
    # purpose: accept steam session cookie input
    # ask user to paste their cookie string (e.g., steamLoginSecure)
    # store it in a variable
    # could optionally persist temporarily in memory
    pass

def validate_session():
    # purpose: optional light check
    # send a minimal request to a steam endpoint that requires authentication
    # if invalid -> notify user and stop program
    # if valid -> proceed
    pass

def get_session_headers():
    # purpose: return a dictionary with headers for authenticated requests
    # include cookie header with the stored session info
    # include standard user-agent if needed
    pass

# optional helper:
def _parse_cookies(cookie_string):
    # convert raw cookie string into dictionary format for requests
    pass

