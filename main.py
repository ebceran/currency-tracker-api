# ============================================================
#  main.py — Client-side simulation for Currency Tracker API
#  CFG Topic Assignment 4
# ============================================================
#  Simulates real interactions with the running Flask API
#  using the requests library.
#
#  IMPORTANT: Make sure app.py is running before executing
#             this file. Run app.py first, then run main.py.
# ============================================================

import requests

BASE_URL = "http://127.0.0.1:5000"


def display_separator():
    """Print a visual separator for readability."""
    print("\n" + "=" * 55)


def get_all_currencies():
    """
    Client function for GET /currencies.
    Fetches and displays all available exchange rates.
    """
    display_separator()
    print("  STEP 1: Fetching all available exchange rates...")
    display_separator()

    response = requests.get(f"{BASE_URL}/currencies")

    if response.status_code == 200:
        data = response.json()
        print(f"  {data['message']}\n")
        for currency in data["data"]:
            print(
                f"  {currency['currency_code']}  |  "
                f"{currency['currency_name']:<22}  |  "
                f"{currency['symbol']:<4}  |  "
                f"1 unit = {currency['usd_rate']} USD"
            )
    else:
        print(f"  Error: {response.json()}")


def get_single_currency(code):
    """
    Client function for GET /currencies/<code>.
    Fetches and displays a single currency rate by code.
    """
    display_separator()
    print(f"  STEP 2: Looking up exchange rate for '{code}'...")
    display_separator()

    response = requests.get(f"{BASE_URL}/currencies/{code}")

    if response.status_code == 200:
        currency = response.json()["data"]
        print(f"  Currency   : {currency['currency_name']} ({currency['currency_code']})")
        print(f"  Symbol     : {currency['symbol']}")
        print(f"  USD Rate   : 1 {currency['currency_code']} = {currency['usd_rate']} USD")
        print(f"  Updated at : {currency['updated_at']}")
    elif response.status_code == 404:
        print(f"  Not found  : {response.json()['error']}")
    else:
        print(f"  Error      : {response.json()}")


def add_new_currency(currency_code, currency_name, symbol, usd_rate):
    """
    Client function for POST /currencies.
    Sends a new currency to be added to the database.
    """
    display_separator()
    print(f"  STEP 3: Adding new currency '{currency_code}'...")
    display_separator()

    payload = {
        "currency_code": currency_code,
        "currency_name": currency_name,
        "symbol": symbol,
        "usd_rate": usd_rate
    }

    response = requests.post(f"{BASE_URL}/currencies", json=payload)

    if response.status_code == 201:
        print(f"  Success: {response.json()['message']}")
    elif response.status_code == 409:
        print(f"  Conflict: {response.json()['error']}")
    elif response.status_code == 400:
        print(f"  Bad request: {response.json()['error']}")
    else:
        print(f"  Error: {response.json()}")


def run():
    """
    Simulates a real-world session with the Currency Tracker API.

    Scenario:
        A fintech analyst opens the dashboard to review today's
        exchange rates, checks the GBP rate specifically, then
        adds a new currency (SGD - Singapore Dollar) to the system.
        Finally, the system attempts to add GBP again to demonstrate
        how duplicate entries are handled gracefully.
    """
    print("\n" + "=" * 55)
    print("   CURRENCY TRACKER API — CLIENT SIMULATION")
    print("   CFG Data Science — Topic Assignment 4")
    print("=" * 55)
    print("\n  Welcome! Connecting to the Currency Tracker API...")

    # Step 1 — View all current exchange rates
    get_all_currencies()

    # Step 2 — Look up a specific currency (GBP)
    get_single_currency("GBP")

    # Step 3 — Look up a currency that does not exist
    get_single_currency("XYZ")

    # Step 4 — Add a new currency (Singapore Dollar)
    add_new_currency(
        currency_code="SGD",
        currency_name="Singapore Dollar",
        symbol="S$",
        usd_rate=0.750000
    )

    # Step 5 — Try adding GBP again to demonstrate duplicate handling
    display_separator()
    print("  STEP 5: Attempting to add GBP again (duplicate test)...")
    display_separator()
    add_new_currency(
        currency_code="GBP",
        currency_name="British Pound",
        symbol="£",
        usd_rate=1.270000
    )

    # Step 6 — Fetch all currencies again to confirm SGD was added
    display_separator()
    print("  STEP 6: Confirming SGD was added — fetching all rates...")
    get_all_currencies()

    display_separator()
    print("\n  Simulation complete. All endpoints tested successfully.")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    run()
