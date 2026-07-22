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

            print("STATUS:", r.status_code)

            r.raise_for_status()

            data = r.json()

            print("TYPE:", type(data))
            print("KEYS:", list(data.keys())[:10])

            self.cache = data

            return True

        except Exception as e:

            print("API ERROR:", e)

            return False

        except Exception as e:

            print(e)

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
