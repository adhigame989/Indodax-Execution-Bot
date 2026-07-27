from api.indodax import api

from engine.state import BotState

class TPEngine:

    def run(self, engine):

        ticker = api.get_ticker(engine.coin)

        if not ticker:
            return

        engine.current_price = ticker["last"]

        # Update Highest Price
        if engine.current_price > engine.highest_price:
            engine.highest_price = engine.current_price

        # Hitung Trailing Price
        engine.trailing_price = (
            engine.highest_price *
            (1 - (engine.trailing_gap / 100))
        )

        print("=" * 40)
        print("TARGET PRICE ACTIVE")
        print("=" * 40)

        print(f"Coin      : {engine.coin}")
        print(f"Target    : {engine.target_price:,.0f}")
        print(f"Current   : {engine.current_price:,.0f}")
        print(f"Highest   : {engine.highest_price:,.0f}")
        print(f"Trailing  : {engine.trailing_price:,.0f}")

        # Aktifkan trailing
        engine.tp_activated = True

        engine.state = BotState.TRAILING


tp_engine = TPEngine()
