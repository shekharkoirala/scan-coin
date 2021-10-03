import os
from dotenv import load_dotenv
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

load_dotenv()

class Bot:
    def __init__(self) -> None:
        api_key = os.getenv('api_key')
        secret_key = os.getenv('secret_key')
        self.biclient = Client(api_key, secret_key)

    def scan(self):
        order_book_data = self.biclient.get_order_book(symbol='DCRUSDT')
        print(order_book_data)



if __name__ == "__main__":
    bibot = Bot()
    bibot.scan()