from data.get_data import update_data_files
from strategies.MACD import buy_sell_stocks_based_on_MACD
from settings import MARKET_DATA_FILE_PATH
def main():
    print("-AlgorithmicTrading START-")
    update_data_files()
    buy_sell_stocks_based_on_MACD(MARKET_DATA_FILE_PATH, 12, 26, 9, 10)
    print("-AlgorithmicTrading FINISH-")


if __name__ == '__main__':
    main()


