import requests
import time

BASE_URL = "https://indodax.com/api"


class IndodaxAPI:

    def __init__(self):
        self.session = requests.Session()
        self.cache = {}
        self.last_update = 0

    def update(self):

        try:

            url = f"{BASE_URL}/ticker_all"

            r = self.session.get(url, timeout=10)

            r.raise_for_status()

            data = r.json()

            if "tickers" not in data:
                print("API ERROR : key 'tickers' tidak ditemukan")
                return False

            self.cache = {}

            for pair, ticker in data["tickers"].items():

                self.cache[pair.lower()] = {
                    "last": float(ticker.get("last", 0)),
                    "buy": float(ticker.get("buy", 0)),
                    "sell": float(ticker.get("sell", 0)),
                    "high": float(ticker.get("high", 0)),
                    "low": float(ticker.get("low", 0)),
                    "vol_idr": float(ticker.get("vol_idr", 0))
                }

            self.last_update = time.time()

            print(f"API OK | Pair Loaded : {len(self.cache)}")

            return True

        except Exception as e:

            print("API ERROR :", e)

            return False

    def get_ticker(self, pair):

        pair = pair.lower()

        return self.cache.get(pair)

    def get_all(self):

        return self.cache

    def is_connected(self):

        return len(self.cache) > 0


api = IndodaxAPI()
