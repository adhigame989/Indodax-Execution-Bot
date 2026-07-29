from engine.state import BotState

class FinishEngine:

    def run(self, engine):

        print("=" * 40)
        print("FINISH ENGINE")
        print("=" * 40)

        print(f"Trade Finished : {engine.coin}")

        # Reset order
        engine.order_id = None
        engine.sell_order_id = None

        # Reset price
        engine.buy_price = 0
        engine.sell_price = 0
        engine.current_price = 0
        engine.entry_price = 0
        engine.highest_price = 0
        engine.trailing_price = 0

        # Reset position
        engine.qty = 0
        engine.buy_time = None
        engine.tp_activated = False

        # Reset trade id
        engine.trade_id = None

        # Jika verify_sell_engine sudah meng-load trade berikutnya,
        # state sudah WAIT_ENTRY.
        # Kalau tidak ada trade lagi, kembali ke STANDBY.
        if engine.coin is None:
            engine.state = BotState.STANDBY

        print("ENGINE RESET COMPLETE")

finish_engine = FinishEngine()
