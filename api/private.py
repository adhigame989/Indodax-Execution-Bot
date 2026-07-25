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

    def get_info(self):

        return self._request("getInfo")


private = PrivateAPI()
