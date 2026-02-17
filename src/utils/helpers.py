# -----------------------------
# Logging helpers
# -----------------------------
def info(message):
    """Prints an informational message."""
    print(f"[INFO] {message}")

def warn(message):
    """Prints a warning message."""
    print(f"[WARN] {message}")

# -----------------------------
# Prompt helpers
# -----------------------------
def prompt_optional_float(prompt_text):
    """
    Prompts the user for a float. Empty input returns None.
    Re-prompts if invalid input.
    """
    while True:
        value = input(prompt_text).strip()
        if value == "":
            return None
        try:
            return float(value)
        except ValueError:
            warn("Invalid number, please enter a valid float or leave blank.")

def prompt_sort_key(allow_game=False):
    """
    Prompts the user for a sort key.
    Returns 'price' or 'name' (and 'game' if allow_game=True).
    Defaults to 'price'.
    """
    valid_keys = ["price", "name"]
    if allow_game:
        valid_keys.append("game")

    key = input(f"Sort by ({'/'.join(valid_keys)}) [price]: ").strip().lower()
    if key not in valid_keys:
        return "price"
    return key
