import time

import config

from api.indodax import api
from engine.state import BotState


class EntryEngine:

    def run(self, engine):

        ticker = api.get_ticker(engine.coin)

        if not ticker:
            return

        engine.current_price = ticker["last"]

        print(
            f"[{engine.coin}] "
            f"Current: {engine.current_price:,.0f} | "
            f"Entry: {engine.entry_price:,.0f}"
        )

        if engine.current_price > engine.entry_price:
            return

        now = time.time()

        if now - engine.last_buy_failed < config.BUY_RETRY_DELAY:

            remain = int(
                config.BUY_RETRY_DELAY -
                (now - engine.last_buy_failed)
            )

            print(f"BUY COOLDOWN ({remain}s)")

            return

        print("=" * 40)
        print("ENTRY TRIGGERED")
        print("=" * 40)

        engine.state = BotState.BUYING


entry_engine = EntryEngine()
