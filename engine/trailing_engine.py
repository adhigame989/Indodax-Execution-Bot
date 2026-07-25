from api.indodax import api

from engine.state import BotState


class TrailingEngine:

    def run(self, engine):

        ticker = api.get_ticker(engine.coin)

        if not ticker:
            return

        engine.current_price = ticker["last"]

        # Update Highest Price
        if engine.current_price > engine.highest_price:

            engine.highest_price = engine.current_price

        # Hitung Trailing Price
        engine.trailing_price = engine.highest_price * (
            1 - (engine.trailing_gap / 100)
        )

        print("=" * 40)
        print("TRAILING ENGINE")
        print("=" * 40)

        print(f"Coin      : {engine.coin}")
        print(f"Current   : {engine.current_price:,.0f}")
        print(f"Highest   : {engine.highest_price:,.0f}")
        print(f"Trailing  : {engine.trailing_price:,.0f}")

        # Harga masih naik
        if engine.current_price > engine.trailing_price:

            print("TRAILING ACTIVE")

            return

        print("=" * 40)
        print("TRAILING STOP HIT")
        print("=" * 40)

        engine.state = BotState.SELLING


trailing_engine = TrailingEngine()
