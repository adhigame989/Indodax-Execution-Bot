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

            self.cache = data["tickers"]

            self.last_update = time.time()

            return True

        except Exception as e:

            print("API ERROR:", e)

            return False

    def get_ticker(self, pair):

        if pair not in self.cache:
            return None

        ticker = self.cache[pair]

        return {
            "last": float(ticker["last"]),
            "buy": float(ticker["buy"]),
            "sell": float(ticker["sell"]),
            "high": float(ticker["high"]),
            "low": float(ticker["low"]),
            "vol_idr": float(ticker["vol_idr"])
        }


api = IndodaxAPI()
