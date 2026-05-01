# ============================================================
#  app.py — Flask API for Currency Tracker
#  CFG Topic Assignment 4
# ============================================================
#  Endpoints:
#    GET  /currencies           → returns all exchange rates
#    GET  /currencies/<code>    → returns one currency by code
#    POST /currencies           → adds a new currency
# ============================================================

from flask import Flask, jsonify, request
from db_utils import get_all_currencies, get_currency_by_code, add_currency

app = Flask(__name__)

# ------------------------------------------------------------
# Endpoint 0: GET /
# Returns a welcome message and basic information about the API.
# Example use: checking if the API is running and discovering available endpoints.
# ------------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Global Currencies API. Track exchange rates against USD.",
        "available_endpoints": {
            "GET all currencies": "/currencies",
            "GET one currency": "/currencies/<currency_code>",
            "POST new currency": "/currencies"
        },
        "example": "/currencies/GBP"
    }), 200

# ------------------------------------------------------------
# Endpoint 1: GET /currencies
# Returns all currency exchange rates stored in the database.
# Example use: displaying all available exchange rates.
# ------------------------------------------------------------
@app.route("/currencies", methods=["GET"])
def get_currencies():
    currencies = get_all_currencies()

    if currencies is None:
        return jsonify({"error": "Failed to retrieve currencies from the database."}), 500

    if len(currencies) == 0:
        return jsonify({"message": "No currencies found.", "data": []}), 200

    return jsonify({
        "message": f"{len(currencies)} currencies found.",
        "data": currencies
    }), 200


# ------------------------------------------------------------
# Endpoint 2: GET /currencies/<code>
# Returns a single currency by its 3-letter code (e.g. GBP).
# Example use: checking the exchange rate for one currency.
# ------------------------------------------------------------
@app.route("/currencies/<string:code>", methods=["GET"])
def get_currency(code):
    currency = get_currency_by_code(code)

    if currency is None:
        return jsonify({"error": f"Currency '{code.upper()}' not found."}), 404

    return jsonify({
        "message": f"Exchange rate for {code.upper()} retrieved successfully.",
        "data": currency
    }), 200


# ------------------------------------------------------------
# Endpoint 3: POST /currencies
# Adds a new currency to the database.
# Expects JSON body: { "currency_code", "currency_name",
#                      "symbol", "usd_rate" }
# Example use: adding a new currency record to the database.
# ------------------------------------------------------------
@app.route("/currencies", methods=["POST"])
def create_currency():
    data = request.get_json()

    # Validate that all required fields are present
    required_fields = ["currency_code", "currency_name", "symbol", "usd_rate"]
    missing = [field for field in required_fields if field not in data]

    if missing:
        return jsonify({
            "error": f"Missing required fields: {', '.join(missing)}"
        }), 400

    # Validate usd_rate is a positive number
    try:
        usd_rate = float(data["usd_rate"])
        if usd_rate <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "usd_rate must be a positive number."}), 400

    success = add_currency(
        currency_code=data["currency_code"],
        currency_name=data["currency_name"],
        symbol=data["symbol"],
        usd_rate=usd_rate
    )

    if not success:
        return jsonify({
            "error": f"Currency '{data['currency_code'].upper()}' already exists or could not be added."
        }), 409

    return jsonify({
        "message": f"Currency '{data['currency_code'].upper()}' added successfully."
    }), 201


# ------------------------------------------------------------
# Run the Flask development server
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
