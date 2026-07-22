import requests

BASE_URL = "https://indodax.com/api"


class IndodaxAPI:

    def __init__(self):
        self.session = requests.Session()

    def get_ticker(self, pair):

        try:

            url = f"{BASE_URL}/{pair}/ticker"

            r = self.session.get(url, timeout=10)

            r.raise_for_status()

            data = r.json()

            return {
                "success": True,
                "last": float(data["ticker"]["last"]),
                "buy": float(data["ticker"]["buy"]),
                "sell": float(data["ticker"]["sell"]),
                "high": float(data["ticker"]["high"]),
                "low": float(data["ticker"]["low"]),
                "vol_idr": float(data["ticker"]["vol_idr"])
            }

        except Exception as e:

            return {
                "success": False,
                "error": str(e)
            }


api = IndodaxAPI()
