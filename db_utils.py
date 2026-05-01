# ============================================================
#  db_utils.py — Database helper functions
#  CFG Topic Assignment 4
# ============================================================
#  This file contains the database connection and query functions.
#  It keeps the MySQL code separate from the Flask routes in app.py.
# ============================================================

import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def get_connection():
    """Create and return a MySQL database connection."""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def get_all_currencies():
    """
    Retrieve all currency exchange rates from the database.
    Returns a list of dictionaries, one per currency.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT currency_code, currency_name, symbol, usd_rate, updated_at
            FROM exchange_rates
            ORDER BY currency_code
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return results

    except mysql.connector.Error as e:
        print(f"Database error in get_all_currencies: {e}")
        return None

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def get_currency_by_code(currency_code):
    """
    Retrieve a single currency by its currency code (e.g. 'GBP').
    Returns a dictionary if found, None if not found or on error.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT currency_code, currency_name, symbol, usd_rate, updated_at
            FROM exchange_rates
            WHERE currency_code = %s
        """
        cursor.execute(query, (currency_code.upper(),))
        result = cursor.fetchone()
        return result

    except mysql.connector.Error as e:
        print(f"Database error in get_currency_by_code: {e}")
        return None

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def add_currency(currency_code, currency_name, symbol, usd_rate):
    """
    Insert a new currency into the database.
    Returns True on success, False if the code already exists or on error.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO exchange_rates (currency_code, currency_name, symbol, usd_rate)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (currency_code.upper(), currency_name, symbol, float(usd_rate)))
        connection.commit()
        return True

    except mysql.connector.IntegrityError:
        # Triggered when the currency_code already exists (UNIQUE constraint)
        print(f"Currency code '{currency_code}' already exists in the database.")
        return False

    except mysql.connector.Error as e:
        print(f"Database error in add_currency: {e}")
        return False

    finally:
        if connection and connection.is_connected():
            if 'cursor' in locals():
                cursor.close()
        connection.close()
