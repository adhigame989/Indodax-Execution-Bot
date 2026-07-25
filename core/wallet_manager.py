from api.private import private


class WalletManager:

    def get_info(self):

        result = private.get_info()

        if result.get("success") != 1:

            return None

        return result["return"]

    def get_balance(self):

        info = self.get_info()

        if info is None:

            return {}

        return info.get("balance", {})

    def get_idr_balance(self):

        balance = self.get_balance()

        return float(balance.get("idr", 0))

    def get_coin_balance(self, coin):

        balance = self.get_balance()

        coin = coin.lower().replace("_idr", "")

        return float(balance.get(coin, 0))

    def can_buy(self, capital):

        return self.get_idr_balance() >= capital

    def can_sell(self, coin, qty):

        return self.get_coin_balance(coin) >= qty


wallet = WalletManager()
