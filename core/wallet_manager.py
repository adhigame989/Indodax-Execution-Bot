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

    def get_coin_balance(coin):
        if not coin:
            return 0

        coin = str(coin).lower().replace("_idr", "")

        try:
            info = private.get_info()

            if not info:
                return 0

            return float(info["balance"].get(coin, 0))

        except Exception:
            return 0
            
    def get_coin_balance(self, coin):

        balance = self.get_balance()

        coin = coin.lower().replace("_idr", "")

        return float(balance.get(coin, 0))

    def get_total_asset(self, coin):

        idr = self.get_idr_balance()

        qty = self.get_coin_balance(coin)

        if qty <= 0:
            return idr

        from api.indodax import api

        ticker = api.get_ticker(coin)

        if ticker is None:
            return idr

        return idr + (qty * ticker["last"])

    def get_wallet_summary(self, coin):

        return {

            "idr": self.get_idr_balance(),

            "coin": self.get_coin_balance(coin),

            "equity": self.get_total_asset(coin)

        }

    def can_buy(self, capital):

        return self.get_idr_balance() >= capital

    def can_sell(self, coin, qty):

        return self.get_coin_balance(coin) >= qty


wallet = WalletManager()
