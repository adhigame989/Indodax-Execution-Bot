import time
import hmac
import hashlib
import urllib.parse
import requests

import config


class PrivateAPI:

    BASE_URL = "https://indodax.com/tapi"

    def __init__(self):

        self.api_key = config.API_KEY
        self.api_secret = config.API_SECRET

        self.session = requests.Session()

    def _request(self, method, params=None):

        if params is None:
            params = {}

        params["method"] = method
        params["nonce"] = str(int(time.time() * 1000))

        body = urllib.parse.urlencode(params)

        signature = hmac.new(
            self.api_secret.encode(),
            body.encode(),
            hashlib.sha512
        ).hexdigest()

        headers = {
            "Key": self.api_key,
            "Sign": signature
        }

        try:

            response = self.session.post(
                self.BASE_URL,
                headers=headers,
                data=params,
                timeout=30
            )

            response.raise_for_status()

            return response.json()

        except Exception as e:

            return {
                "success": 0,
                "error": str(e)
            }

    # ==========================
    # ACCOUNT
    # ==========================

    def get_info(self):

        return self._request(
            "getInfo"
        )

    # ==========================
    # BUY
    # ==========================

    def buy(self, pair, price, idr):

        return self._request(

            "trade",

            {

                "pair": pair.lower(),

                "type": "buy",

                "price": price,

                "idr": idr

            }

        )

    # ==========================
    # SELL
    # ==========================

    def sell(self, pair, price, coin):

        return self._request(

            "trade",

            {

                "pair": pair.lower(),

                "type": "sell",

                "price": price,

                pair.lower().replace("_idr", ""): coin

            }

        )

    # ==========================
    # ORDER STATUS
    # ==========================

    def get_order(self, pair, order_id):

        return self._request(

            "getOrder",

            {

                "pair": pair.lower(),

                "order_id": order_id

            }

        )

    # ==========================
    # OPEN ORDER
    # ==========================

    def open_orders(self, pair):

        return self._request(

            "openOrders",

            {

                "pair": pair.lower()

            }

        )

    # ==========================
    # CANCEL ORDER
    # ==========================

    def cancel_order(self, pair, order_id, order_type):

        return self._request(

            "cancelOrder",

            {

                "pair": pair.lower(),

                "order_id": order_id,

                "type": order_type

            }

        )


private = PrivateAPI()
