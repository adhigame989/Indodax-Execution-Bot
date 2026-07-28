from engine.state import BotState
from engine.order import order
from core.position_manager import position_manager
from datetime import datetime

class VerifyBuyEngine:

    def run(self, engine):

        print("=" * 40)
        print("VERIFY BUY ENGINE")
        print("=" * 40)

        verify = order.verify_buy(

            engine.coin,

            engine.order_id

        )
        print("VERIFY RESULT =", verify)

        if not verify["success"]:

            print(
                verify.get(
                    "message",
                    "VERIFY BUY FAILED"
                )
            )

            return

        if not verify["filled"]:

            print("WAIT BUY FILL")

            return

        engine.buy_price = float(verify["price"])

        engine.highest_price = engine.buy_price

        engine.qty = float(verify["qty"])

        print(">>> CREATE ACTIVE POSITION <<<")

        position_manager.add(

            coin=engine.coin,

            buy_price=engine.buy_price,

            capital=engine.capital,

            qty=engine.qty

            target_price=engine.target_price

        )

        print("=" * 40)
        print("BUY VERIFIED")
        print(f"Coin : {engine.coin}")
        print(f"Buy  : {engine.buy_price:,.0f}")
        print(f"Qty  : {engine.qty}")
        print("=" * 40)

        engine.buy_time = datetime.now()
        engine.state = BotState.HOLDING
        
        print(">>> STATE CHANGED TO HOLDING <<<")


verify_buy_engine = VerifyBuyEngine()
