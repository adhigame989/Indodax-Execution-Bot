import threading
import time

from engine.state import BotState


class ExecutionEngine:

    def __init__(self):

        self.state = BotState.STANDBY

        self.running = False

        self.thread = None

        self.interval = 1

        self.coin = None

        self.entry_price = 0

        self.take_profit = 0

        self.trailing_gap = 0

        self.capital = 0

    def configure(
        self,
        coin,
        entry_price,
        take_profit,
        trailing_gap,
        capital
    ):

        self.coin = coin.upper()

        self.entry_price = float(entry_price)

        self.take_profit = float(take_profit)

        self.trailing_gap = float(trailing_gap)

        self.capital = float(capital)

        self.state = BotState.WAIT_ENTRY

        print("ENGINE CONFIGURED")

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.loop,
            daemon=True
        )

        self.thread.start()

        print("EXECUTION ENGINE STARTED")

    def stop(self):

        self.running = False

        self.state = BotState.PAUSED

        print("EXECUTION ENGINE STOPPED")

    def loop(self):

        while self.running:

            print(f"STATE : {self.state.value}")

            time.sleep(self.interval)

    def get_status(self):

        return {

            "state": self.state.value,

            "coin": self.coin,

            "entry_price": self.entry_price,

            "take_profit": self.take_profit,

            "trailing_gap": self.trailing_gap,

            "capital": self.capital

        }


engine = ExecutionEngine()
