from logging import logMultiprocessing
import os, time
from dotenv import load_dotenv
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

load_dotenv()

class Bot:
    def __init__(self) -> None:
        api_key = os.getenv('api_key')
        secret_key = os.getenv('secret_key')
        self.biclient = Client(api_key, secret_key)
        self.total_coins = 0

    def get_usdt_coins(self):
        """get usdt coins symbol and price

        Returns:
            [list]: eg: [{'symbol': 'SYSUSDT', 'price': '0.30610000'},{'symbol': 'FIDAUSDT', 'price': '7.23300000'}]
        """
        all_coin = self.biclient.get_all_tickers() 
        selected_coin = [ coin["symbol"] for coin in all_coin if coin["symbol"][-4:] == "USDT" and coin["symbol"][-6:] != "UPUSDT" and coin["symbol"][-8:] != "DOWNUSDT"]
        self.total_coins =  len(selected_coin)
        return selected_coin

    def get_historical_data(self, coin_name):
        """[summary]

                    1499040000000,      # Open time
                    "0.01634790",       # Open
                    "0.80000000",       # High
                    "0.01575800",       # Low
                    "0.01577100",       # Close
                    "148976.11427815",  # Volume
                    1499644799999,      # Close time
                    "2434.19055334",    # Quote asset volume
                    308,                # Number of trades
                    "1756.87402397",    # Taker buy base asset volume
                    "28.46694368",      # Taker buy quote asset volume
                    "17928899.62484339" # Can be ignored
                ]
        iN ASCENDING DATE TIME.
        """
        candles = self.biclient.get_klines(symbol=coin_name, interval=Client.KLINE_INTERVAL_1HOUR, limit =4)
        return candles
    
    def logic(self, history_data):
        """ test purpose only.
        """
        differences = [round(float(history_data[i][4]) - float(history_data[i-1][4]), 3) for i in range(1, len(history_data))]
        return differences, all(i<0 for i in differences)

    def process(self):
        for i , coin in enumerate(self.get_usdt_coins()):
            data= self.get_historical_data(coin)
            differences, status = self.logic(data)
            if status:
                print(coin, differences)
            print(f"checking {i} / {self.total_coins}")
    

if __name__ == "__main__":
    s = time.time()
    bibot = Bot()
    bibot.process()
    print(f"{time.time() -s } seconds")