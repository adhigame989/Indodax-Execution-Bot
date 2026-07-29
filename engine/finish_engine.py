from engine.state import BotState
from core.trade_manager import trade_manager

class FinishEngine:

    def run(self, engine):

        print("=" * 40)
        print("FINISH ENGINE")
        print("=" * 40)

        print(f"Trade Finished : {engine.coin}")

        # Reset order
        engine.order_id = None
        engine.sell_order_id = None

        # Reset trading data
        engine.buy_price = 0
        engine.sell_price = 0
        engine.current_price = 0
        engine.highest_price = 0
        engine.trailing_price = 0

        engine.qty = 0
        engine.buy_time = None
        engine.tp_activated = False

        # Hapus data trade lama
        engine.coin = None
        engine.entry_price = 0
        engine.target_price = 0
        engine.capital = 0
        engine.trade_id = None

        # Ambil trade berikutnya
        trade = trade_manager.get_next_waiting_trade()

        if trade:

            print(f"LOAD NEXT TRADE : {trade['coin']}")

            engine.configure(
                coin=trade["coin"],
                entry_price=trade["entry_price"],
                target_price=trade["target_price"],
                trailing_gap=trade["trailing_gap"],
                capital=trade["capital"],
                trade_id=trade["id"]
            )

            print("NEXT TRADE READY")

        else:

            engine.state = BotState.STANDBY

            print("NO WAITING TRADE")

finish_engine = FinishEngine()
