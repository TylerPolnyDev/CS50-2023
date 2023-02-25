import json
import requests
import sqlite3
import pandas as pd
import ssl
import time
import traceback
# Alpha Vantage API key
from settings import ALPHA_VANTAGE_API_KEY, ALPACA_API_KEY, ALPACA_SECRET_KEY, MARKET_DATA_FILE_PATH, PORTFOLIO_FILE_PATH





def get_symbols_SP500():
    print("Collecting stock symbols for S&P 500 from Wikipedia...")
    ssl._create_default_https_context = ssl._create_unverified_context
    URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    symbols = pd.read_html(URL)[0]['Symbol'].tolist()
    return symbols


def get_market_data(symbols):
    print("Collecting market data for each symbol in S&P 500...")
    print("\nExpect a 12 second delay in between each stock symbol data collection.\nManual sleep applied to meet rate limiting requirments of alphavantage.\nExpect market data collection to take up to 1.6 hours.")

    # Load the existing market data from market_data.json
    with open(MARKET_DATA_FILE_PATH, 'r') as jsonfile:
        data = json.load(jsonfile)

    # For each symbol, check if it is already in the data, and update it if it is
    symbolsProcessed = 0
    for symbol in symbols:
        try:
            #TODO: replace hard coded "503" with a list count value from get_symbols_SP500
            progress = round((symbolsProcessed / 503) * 100)
            print("\n\nData Collection Progress: %" + str(progress))
            if symbol == "BF.B":
                symbol = "BF-B"
            url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
            response = requests.get(url)
            marketData = response.json()
            if "Meta Data" in marketData:
                metaData = marketData["Meta Data"]
                stockSymbol = metaData["2. Symbol"]
                newTimeSeriesDaily = marketData["Time Series (Daily)"]
                print("collecting data for...")
                print("Symbol: "+str(stockSymbol))
                if stockSymbol in data:
                    # Update the existing data for the symbol by merging the new data for timeSeriesDaily with the existing data, and removing duplicates
                    existingTimeSeriesDaily = data[stockSymbol]
                    combinedTimeSeriesDaily = {**existingTimeSeriesDaily, **newTimeSeriesDaily}
                    data[stockSymbol] = combinedTimeSeriesDaily
                else:
                    # Add the new data for the symbol
                    data[stockSymbol] = newTimeSeriesDaily
            else:
                print("Error for symbol "+str(stockSymbol))
                print("data returned:")
                print(marketData)
            time.sleep(12)
            symbolsProcessed = symbolsProcessed + 1
        except Exception:
            print("caught exception processing market_data.json")
            traceback.print_exc()
            print("caught exception processing market_data.json")


    # Save the updated data to market_data.json
    with open(MARKET_DATA_FILE_PATH, 'w') as jsonfile:
        json.dump(data, jsonfile)
    print("Market data collection complete!")

#TODO: create a function to call alpaca API to get data for portfolio.db
#TODO: create a function "get_news_data" which will for each symbol look for any news articals posted in the last 24 hours for that symbol.

#TODO: create a function "get_social_media_data" which will for each symbol look up their social media accounts and add it to social_media.json.


def populate_portfolio_db():
    print("Updating portfolio.db with current holdings...")

    # Make a request to the Alpaca API to get the data of your stock holdings
    headers = {
        'APCA-API-KEY-ID': ALPACA_API_KEY,
        'APCA-API-SECRET-KEY': ALPACA_SECRET_KEY
    }
    r = requests.get('https://paper-api.alpaca.markets/v2/positions', headers=headers)
    stock_holdings_data_json = r.text
    print(stock_holdings_data_json)
    stock_holdings_data = json.loads(stock_holdings_data_json)
    # Create a connection to the portfolio.db database
    conn = sqlite3.connect(PORTFOLIO_FILE_PATH)
    conn.isolation_level = None

    # Create the stock_holdings table in the database
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stock_holdings (
            symbol text,
            quantity real,
            market_value real,
            avg_entry_price real,
            unrealized_pl real,
            unrealized_plpc real,
            holding_period datetime
        );
        """
    )
    conn.commit()
    cursor.close()

    # Get a list of symbols in the stock_holdings_data
    symbols_in_stock_holdings_data = [holding["symbol"] for holding in stock_holdings_data]

    # Get a list of symbols in the stock_holdings table
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT symbol FROM stock_holdings
        """
    )
    symbols_in_stock_holdings_table = [row[0] for row in cursor.fetchall()]
    cursor.close()

    # Delete symbols that are in the stock_holdings table but not in the stock_holdings_data
    symbols_to_delete = set(symbols_in_stock_holdings_table) - set(symbols_in_stock_holdings_data)
    for symbol in symbols_to_delete:
        cursor = conn.cursor()
        cursor.execute(
            """
            DELETE FROM stock_holdings WHERE symbol=?
            """,
            (symbol,)
        )
        conn.commit()
        cursor.close()

    # Iterate through the data of your stock holdings and insert each stock holding into the stock_holdings table
    for holding in stock_holdings_data:
        symbol = holding["symbol"]
        quantity = holding["qty"]
        market_value = holding["market_value"]
        avg_entry_price = holding["avg_entry_price"]
        unrealized_pl = holding["unrealized_pl"]
        unrealized_plpc = holding["unrealized_plpc"]
        # Check if the stock symbol is already present in the stock_holdings table
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM stock_holdings WHERE symbol=?
            """,
            (symbol,)
        )
        result = cursor.fetchone()
        cursor.close()

        # If the stock symbol is already present, update the quantity, market value, average entry price,
        # unrealized profit/loss, and unrealized profit/loss per share values for that symbol
        if result is not None:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE stock_holdings
                SET quantity=?, market_value=?, avg_entry_price=?, unrealized_pl=?, unrealized_plpc=?
                WHERE symbol=?
                """,
                (quantity, market_value, avg_entry_price, unrealized_pl, unrealized_plpc, symbol)
            )
            conn.commit()
            cursor.close()
        # If the stock symbol is not present, insert a new row into the stock_holdings table
        # with the symbol, quantity, market value, average entry price, unrealized profit/loss, and unrealized profit/loss per share values
        else:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO stock_holdings (symbol, quantity, market_value, avg_entry_price, unrealized_pl, unrealized_plpc)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (symbol, quantity, market_value, avg_entry_price, unrealized_pl, unrealized_plpc)
            )
            conn.commit()
            cursor.close()
    conn.close()
    print("portfolio.db is up to date!")


def update_data_files():
    symbols = get_symbols_SP500()
    get_market_data(symbols)
    populate_portfolio_db()

def main():
    print('module testing for MACD.py starts here')
    print('testing get_symbols_SP500...')
    symbols = get_symbols_SP500()
    print('testing get_market_data...')
    get_market_data(symbols)
    print('testing populate_portfolio_db...')
    populate_portfolio_db()

if __name__ == '__main__':
  main()
