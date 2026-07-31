from api.indodax import api
from engine.state import BotState
from core.position_manager import position_manager
from core.wallet_manager import wallet


class HoldingEngine:

    def run(self, engine):

        ticker = api.get_ticker(engine.coin)

        if not ticker:
            return

        coin_symbol = engine.coin.replace("_IDR", "").lower()

        balance = wallet.get_coin_balance(
            coin_symbol
        )

        if balance <= 0:

            print("=" * 40)
            print(
                f"MANUAL SELL DETECTED | "
                f"{engine.coin} balance={balance}"
            )
            print("=" * 40)

            position_manager.remove(
                engine.coin
            )

            engine.state = BotState.FINISHED

            return
        engine.current_price = ticker["last"]

        # Update Highest Price
        if engine.current_price > engine.highest_price:

            engine.highest_price = engine.current_price

            position_manager.update_highest(

                engine.coin,

                engine.highest_price

            )

        print("=" * 40)

        print("HOLDING")

        print("=" * 40)

        print(f"Coin    : {engine.coin}")

        print(f"Buy     : {engine.buy_price:,.0f}")

        print(f"Current : {engine.current_price:,.0f}")

        print(f"Highest : {engine.highest_price:,.0f}")

        print(f"Target  : {engine.target_price:,.0f}")

        # Target Price tercapai

        if (
            engine.target_price > 0
            and
            engine.current_price >= engine.target_price
        ):

            print("=" * 40)

            print("TARGET PRICE REACHED")

            print("=" * 40)

            engine.state = BotState.TP_ZONE


holding_engine = HoldingEngine()
