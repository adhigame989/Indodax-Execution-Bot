from engine.state import BotState
from engine.order import order
from core.position_manager import position_manager
from core.trade_manager import trade_manager

class VerifySellEngine:

    def run(self, engine):

        print("=" * 40)
        print("VERIFY SELL ENGINE")
        print("=" * 40)

        verify = order.verify_sell(

            engine.coin,

            engine.sell_order_id

        )

        if not verify["success"]:

            print(

                verify.get(

                    "message",

                    "VERIFY SELL FAILED"

                )

            )

            return

        if not verify["filled"]:

            if (
                engine.sell_verify_started and
                time.time() - engine.sell_verify_started > 300
            ):

                print("SELL VERIFY TIMEOUT")

                order.cancel(
                    engine.coin,
                    engine.sell_order_id,
                    "sell"
                )

                engine.sell_order_id = None
                engine.sell_verify_started = None

                engine.state = BotState.HOLDING

                return

            print("WAIT SELL FILL")

            return

        sell_price = float(verify["price"])

        pnl = (

            (sell_price - engine.buy_price)

            * engine.qty

        )

        print("=" * 40)
        print("SELL VERIFIED")
        print("=" * 40)

        print(f"Coin : {engine.coin}")

        print(f"Sell : {sell_price:,.0f}")

        print(f"Qty  : {engine.qty}")

        print(f"P/L  : {pnl:,.0f}")

        position_manager.remove(
            engine.coin
        )

        engine.sell_price = sell_price

# Tandai trade selesai
        if engine.trade_id:
            trade_manager.set_status(
                engine.trade_id,
                "FINISHED"
            )
        engine.state = BotState.FINISHED

verify_sell_engine = VerifySellEngine()
