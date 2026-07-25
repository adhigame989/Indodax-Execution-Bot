from engine.state import BotState


class FinishEngine:

    def run(self, engine):

        print("=" * 40)
        print("FINISH ENGINE")
        print("=" * 40)

        print(f"Trade Finished : {engine.coin}")

        # Reset Trading Variable
        engine.order_id = None
        engine.sell_order_id = None

        engine.buy_price = 0
        engine.sell_price = 0

        engine.current_price = 0
        engine.entry_price = 0

        engine.highest_price = 0
        engine.trailing_price = 0

        engine.qty = 0

        engine.tp_activated = False

        engine.state = BotState.WAIT_ENTRY

        print("READY FOR NEXT TRADE")


finish_engine = FinishEngine()
