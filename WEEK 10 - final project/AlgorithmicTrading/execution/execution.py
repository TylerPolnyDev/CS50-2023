from settings import ALPACA_API_KEY, ALPACA_SECRET_KEY, PORTFOLIO_FILE_PATH
import requests
import time
from data.get_data import populate_portfolio_db
import sqlite3

# Set the base URL for the Alpaca API
BASE_URL = "https://paper-api.alpaca.markets"

# Set the headers for the HTTP request
headers = {
    "APCA-API-KEY-ID": ALPACA_API_KEY,
    "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
}


def QTY_buy_stocks(symbol, qty):
    """
    Buy stocks using the Alpaca API.
    """
    # Set the endpoint for the POST /v2/orders request
    endpoint = f"{BASE_URL}/v2/orders"

    # Set the payload for the request
    payload = {
        "symbol": symbol,
        "qty": str(qty),
        "side": "buy",
        "type": "market",
        "time_in_force": "day"
    }

    # Make the HTTP POST request
    response = requests.post(endpoint, json=payload, headers=headers)

    # If the request was successful, return the order details
    if response.status_code == 200:
        populate_portfolio_db()
        return response.json()
    else:
        print(f"Failed to buy stocks: {response.text}")




def QTY_sell_stocks(symbol, qty):
    """
    Sell stocks using the Alpaca API.
    """
    # Connect to the database
    conn = sqlite3.connect(PORTFOLIO_FILE_PATH)
    c = conn.cursor()

    # Check if the symbol is in the portfolio
    c.execute("SELECT * FROM stock_holdings WHERE symbol=?", (symbol,))
    symbol_data = c.fetchone()
    if symbol_data is None:
        print("Failed to sell stocks: stocks not in portfolio.db")
        return
    else:
        print(symbol_data[1])

    # Check if the quantity of the symbol in the portfolio is greater than or equal to the quantity being sold
    if symbol_data[1] < qty:
        print("Failed to sell stocks: insufficient quantity in portfolio.db")
        return
    # Set the endpoint for the POST /v2/orders request
    endpoint = f"{BASE_URL}/v2/orders"

    # Set the payload for the request
    payload = {
        "symbol": symbol,
        "qty": str(qty),
        "side": "sell",
        "type": "market",
        "time_in_force": "day"
    }

    # Make the HTTP POST request
    response = requests.post(endpoint, json=payload, headers=headers)

    # If the request was successful, return the order details
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to sell stocks: {response.text}")


def VAL_buy_stocks(symbol, dollar_amount):
    """
    Buy stocks using the Alpaca API.
    """
    # Set the endpoint for the POST /v2/orders request
    endpoint = f"{BASE_URL}/v2/orders"

    # Set the payload for the request
    payload = {
        "symbol": symbol,
        "notional": str(dollar_amount),
        "side": "buy",
        "type": "market",
        "time_in_force": "day"
    }

    # Make the HTTP POST request
    response = requests.post(endpoint, json=payload, headers=headers)

    # If the request was successful, return the order details
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to buy stocks: {response.text}")


def VAL_sell_stocks(symbol, dollar_amount):
    """
    Sell stocks using the Alpaca API.
    """
    populate_portfolio_db()
    # Connect to the database
    conn = sqlite3.connect(PORTFOLIO_FILE_PATH)
    c = conn.cursor()

    # Check if the symbol is in the portfolio
    c.execute("SELECT * FROM stock_holdings WHERE symbol=?", (symbol,))
    symbol_data = c.fetchone()
    if symbol_data is None:
        print("Failed to sell stocks: stocks not in portfolio.db")
        return
    else:
        print(symbol_data[2])

    # Check if the quantity of the symbol in the portfolio is greater than or equal to the quantity being sold
    if symbol_data[2] < dollar_amount:
        print("Failed to sell stocks: insufficient value in portfolio.db")
        return

    # Set the endpoint for the POST /v2/orders request
    endpoint = f"{BASE_URL}/v2/orders"

    # Set the payload for the request
    payload = {
        "symbol": symbol,
        "notional": str(dollar_amount),
        "side": "sell",
        "type": "market",
        "time_in_force": "day"
    }

    # Make the HTTP POST request
    response = requests.post(endpoint, json=payload, headers=headers)

    # If the request was successful, return the order details
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to sell stocks: {response.text}")


def main():
    ##print('module testing for execution.py starts here')
    ##print("attempting to buy qty 5 of AAL")
    # VAL_buy_stocks("AAL",'5')

    # print('attempting to sell qty 20 of AAPL')
    # VAL_sell_stocks("AAPL",'20')
    # print('module testing for execution.py ends here')
    QTY_sell_stocks("AAL", 2)


if __name__ == '__main__':
    main()
