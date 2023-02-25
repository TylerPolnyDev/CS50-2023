# Algorithmic Trading
#### Video Demo:  <https://youtu.be/kiSL6u0rzhs>
#### Description:
The Algorithmic Trading System (ATS) will autonomously monitor and manage your stock portfolio. This program utilizes Alpaca API to buy and sell stocks, and Alphavantage API to obtain market data. The ATS starts by parsing the stock symbole for each of the S&P 500 from Wikipedia. It then uses Alphavantage API to populate market_data.json with data for each symbole. After it uses Alpaca API to populate portfolio.db with the users current stock holdings. Finally the ATS will implement strategies out of the strategies directory (with MACD being the only active strategy at this time). If a strategy determines a stock is qualified to either be sold or purchased, it will call the execution directory to place the order using Alpaca API.

#### Installation:
1. Visit https://alpaca.markets/ and set up a free account and collect your ALPACA_ACCOUNT_ID, ALPACA_SECRET_KEY, and ALPACA_API_KEY

NOTE: it is strongly advised to start with the PAPER TRADING API KEY. This is for educational use only
2. Visit https://www.alphavantage.co/support/#api-key and set up a free account and collect your ALPHA_VANTAGE_API_KEY
3. In this program, copy the FULL FILE PATH to "market_data.json" and "portfolio.db"
4. In AlgorithmicTrading/settings.py, set the values for ALPHA_VANTAGE_API_KEY, ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_ACCOUNT_ID, MARKET_DATA_FILE_PATH, and PORTFOLIO_FILE_PATH to the values collected in step 1-3
5. If on linux, set this program up to excute on a cron, once daily at midnight.
####AI
TODO this will keep track of which trades where positive or negative, and will adjust values for hold times, signal lines, and other values throughout strategies.
####backtesting:
TODO This directory will be used to hold programs to test new strategies before using them outside of paper trading. It will make use of past market data to determine if a strategy had been profitable if applied on a past date.

####data:
This directory is used to hold data files, as well as hold .py files responsible for populating said data files. I make use of a sqlite3 DB for portfolio data as it changes regularly through the programs operation, and a .json file for market data, as this past data is static and is iterated through start to finish.

####execution:
Contain files used to execute buy and sell orders using Alpaca API.

###Strategies
####MACD.py
this class makes use of the Moving Average Convergence Divergence (MACD) technical analysis indicator. The MACD is calculated using two exponential moving averages (EMAs) of different time periods, and a signal line is plotted on top of the MACD line to generate trading signals.
Once the MACD and signal line have been calculated, the function checks whether the MACD line is above or below the signal line.
If the MACD line is above the signal line, it is interpreted as a bullish signal, and the function buys $5 worth of the stock using the VAL_buy_stocks() function.
if the MACD line is below the signal line, it is interpreted as a bearish signal, and the function checks whether the stock has been held for a specified holding_period before selling all of the stock using the QTY_sell_stocks() function.

####portfolio_rebalancing.py
TODO This class will run after all strategies have been applied.
This script implements a portfolio rebalancing algorithm that ensures that the current value of each stock in the portfolio is approximately equal to a target value. The script reads the current holdings in the portfolio from a SQLite database, and calculates the current market value of each holding based on the latest market price data. It then computes the target value of each holding based on the total portfolio value and the desired target percentage for each holding. If the actual value of a holding deviates from the target value by more than a specified threshold, the script generates a buy or sell order to rebalance the holding.
