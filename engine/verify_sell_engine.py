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
                "COMPLETED"
            )

# Ambil trade berikutnya
        trade = trade_manager.get_next_waiting_trade()

        if trade:

            print(f"NEXT TRADE : {trade['coin']}")

            engine.configure(
                coin=trade["coin"],
                entry_price=trade["entry_price"],
                target_price=trade["target_price"],
                trailing_gap=trade["trailing_gap"],
                capital=trade["capital"],
                trade_id=trade["id"]
            )

        else:

                engine.state = BotState.FINISHED


verify_sell_engine = VerifySellEngine()
