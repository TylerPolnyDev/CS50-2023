import json
import sqlite3
from datetime import datetime, timedelta
from execution import execution
from data import get_data
from settings import MARKET_DATA_FILE_PATH, PORTFOLIO_FILE_PATH


def calculate_MACD(prices, short_window, long_window):
    # Calculate the short and long exponential moving averages
    short_EMA = calculate_EMA(prices, short_window)
    long_EMA = calculate_EMA(prices, long_window)

    # Subtract the long EMA from the short EMA to get the MACD
    MACD = [short_EMA[i] - long_EMA[i] for i in range(len(short_EMA))]

    return MACD


def calculate_signal_line(MACD, signal_window):
    # Calculate the signal line by taking the exponential moving average of the MACD
    signal_line = calculate_EMA(MACD, signal_window)

    return signal_line


def calculate_EMA(prices, window):
    # Calculate the exponential moving average
    ##print("value being given to calculate_EMA as prices")
    ##print(prices)
    EMA = []
    alpha = 2 / (window + 1)
    if isinstance(prices,float):
        EMA = [prices * alpha]
        ##print(EMA)
    else:
        for i in range(len(prices)):
            if i == 0:
                EMA.append(float(prices[i]))
            else:
                EMA.append((float(prices[i]) * alpha) + (EMA[-1] * (1 - alpha)))
            ##print(EMA)
    return EMA




def buy_sell_stocks_based_on_MACD(market_data_file, short_window, long_window, signal_window, holding_period):
    # Read in the market data from the JSON file
    print("Executing MACD strategy to S&P500...")
    conn = sqlite3.connect(PORTFOLIO_FILE_PATH)
    holding_period_date = (datetime.now() - timedelta(days=holding_period))
    today = datetime.now()
    with open(market_data_file, 'r') as f:
        market_data = json.load(f)
        for stock_ticker, daily_prices in market_data.items():
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT holding_period FROM stock_holdings WHERE symbol=?
                """,
                (stock_ticker,)
            )
            applied_holding_period = cursor.fetchone()
            cursor.close()
            print("\n\nChecking "+str(stock_ticker)+" using MACD.py")
            # Convert the daily prices to a list of floating point values
            prices = []
            for date in daily_prices:
                prices += [daily_prices[date]['4. close']]
            #print("daily closing prices for "+str(stock_ticker)+":")
            #print(prices)
            # Calculate the MACD and signal line for the stock
            MACD = calculate_MACD(prices, short_window, long_window)
            #print("MACD: "+str(MACD))
            signal_line = calculate_signal_line(MACD, signal_window)
            #print("signal line: "+str(signal_line))
            # If the MACD is above the signal line, buy the stock
            if MACD[-1] > signal_line[-1]:
                print("MACD > Signal line - Buying $5 worth of "+str(stock_ticker))
                execution.VAL_buy_stocks(stock_ticker, 5)
                cursor = conn.cursor()
                cursor.execute(
                    """
                    UPDATE stock_holdings
                    SET holding_period=?
                    WHERE symbol=?
                    """,
                    (holding_period_date, stock_ticker)
                )
                cursor.close()

            # If the MACD is below the signal line, sell the stock
            elif MACD[-1] < signal_line[-1]:
                doneHolding = False
                print("value for holding period:")
                print(applied_holding_period)
                if (applied_holding_period is None):
                    doneHolding = True
                elif(type(applied_holding_period) == tuple):
                    if ((len(applied_holding_period) == 1) & (applied_holding_period[0] == None)):
                        doneHolding = True
                elif(today > applied_holding_period):
                    doneHolding = True

                if (doneHolding == True):
                    # Check if the stock exists in the stock_holdings table in the portfolio database
                    cursor = conn.cursor()
                    cursor.execute("SELECT quantity FROM stock_holdings WHERE symbol=?", (stock_ticker,))
                    result = cursor.fetchone()
                    cursor.close()
                    if result is not None:
                        print("MACD < Signal line - Selling all stock for " + str(stock_ticker))
                        qty_in_portfolio = result[0]
                        execution.QTY_sell_stocks(stock_ticker, qty_in_portfolio)
        conn.close()
        print("Execution of MACD strategy is complete!")
        get_data.populate_portfolio_db()


def main():
  print('module testing for MACD.py starts here')
  buy_sell_stocks_based_on_MACD(MARKET_DATA_FILE_PATH, 12, 26, 9, 10)




if __name__ == '__main__':
  main()
