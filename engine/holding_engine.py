from api.indodax import api

from engine.state import BotState
from core.position_manager import position_manager


class HoldingEngine:

    def run(self, engine):

        ticker = api.get_ticker(engine.coin)

        if not ticker:
            return

        engine.current_price = ticker["last"]

        # Update Highest Price
        if engine.current_price > engine.highest_price:

            engine.highest_price = engine.current_price

            position_manager.update_highest(

                engine.coin,

                engine.highest_price

            )

        # Hitung Profit %
        profit = (

            (engine.current_price - engine.buy_price)

            / engine.buy_price

        ) * 100

        print("=" * 40)

        print("HOLDING")

        print("=" * 40)

        print(f"Coin    : {engine.coin}")

        print(f"Buy     : {engine.buy_price:,.0f}")

        print(f"Current : {engine.current_price:,.0f}")

        print(f"Highest : {engine.highest_price:,.0f}")

        print(f"Profit  : {profit:.2f}%")

        # Masuk TP Zone
        if profit >= engine.take_profit:

            print("=" * 40)

            print("TP ZONE REACHED")

            print("=" * 40)

            engine.state = BotState.TP_ZONE


holding_engine = HoldingEngine()
