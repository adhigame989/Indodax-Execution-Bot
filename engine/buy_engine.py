import time

from engine.state import BotState
from engine.order import order
from core.wallet_manager import wallet


class BuyEngine:

    def run(self, engine):

        print("=" * 40)
        print("BUY ENGINE")
        print("=" * 40)

        # Cek saldo IDR
        if not wallet.can_buy(engine.capital):

            print("BUY FAILED : Insufficient IDR Balance")

            engine.last_buy_failed = time.time()

            engine.state = BotState.WAIT_ENTRY

            return

        # Kirim Buy Order
        result = order.buy(

            engine.coin,

            engine.entry_price,

            engine.capital

        )

        if result["success"]:

            engine.order_id = result["order_id"]

            print(f"BUY ORDER CREATED : {engine.order_id}")

            engine.state = BotState.VERIFY_BUY

        else:

            print(result.get("message", "BUY FAILED"))

            engine.last_buy_failed = time.time()

            engine.state = BotState.WAIT_ENTRY


buy_engine = BuyEngine()
