import time


class OrderEngine:

    def buy(self, coin, price, capital):

        print("=" * 40)
        print("BUY ORDER")
        print("=" * 40)

        print(f"Coin    : {coin}")
        print(f"Price   : {price}")
        print(f"Capital : {capital}")

        time.sleep(1)

        print("BUY SUCCESS (SIMULATION)")

        return {

            "success": True,

            "price": price,

            "capital": capital

        }


    def sell(self, coin, price):

        print("=" * 40)
        print("SELL ORDER")
        print("=" * 40)

        print(f"Coin  : {coin}")
        print(f"Price : {price}")

        time.sleep(1)

        print("SELL SUCCESS (SIMULATION)")

        return {

            "success": True,

            "price": price

        }

    def verify(self):

        print("VERIFY ORDER (SIMULATION)")

        return {

            "status": "SUCCESS"

        }


order = OrderEngine()
