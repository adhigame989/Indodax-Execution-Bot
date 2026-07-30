from engine.state import BotState
from engine.order import order
from core.wallet_manager import wallet


class SellEngine:

    def run(self, engine):

        print("=" * 40)
        print("SELL ENGINE")
        print("=" * 40)

        qty = engine.qty

        if qty <= 0:

            print("SELL FAILED : INVALID QTY")

            engine.state = BotState.HOLDING

            return

        if not wallet.can_sell(

            engine.coin,

            qty

        ):

            print("SELL FAILED : Coin Balance Not Enough")

            engine.state = BotState.HOLDING

            return

        result = order.sell(

            engine.coin,

            engine.current_price,

            qty

        )

        if result["success"]:

            engine.sell_order_id = result["order_id"]

            engine.sell_verify_started = time.time()

            print(

                f"SELL ORDER CREATED : {engine.sell_order_id}"

            )

            engine.state = BotState.VERIFY_SELL

        else:

            print(

                result.get(

                    "message",

                    "SELL FAILED"

                )

            )

            engine.state = BotState.HOLDING


sell_engine = SellEngine()
