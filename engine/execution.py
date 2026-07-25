import threading
import time

from engine.state import BotState
from engine.entry_engine import entry_engine
from engine.buy_engine import buy_engine
from engine.verify_buy_engine import verify_buy_engine
from engine.holding_engine import holding_engine
from engine.tp_engine import tp_engine
from engine.trailing_engine import trailing_engine
from engine.sell_engine import sell_engine
from engine.verify_sell_engine import verify_sell_engine
from engine.finish_engine import finish_engine

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
        self.buy_price = 0
        self.sell_price = 0
        self.qty = 0
        self.current_price = 0
        self.highest_price = 0
        self.trailing_price = 0
        self.tp_activated = False
        self.order_id = None
        self.sell_order_id = None
        self.last_buy_failed = 0
        self.buy_time = None

    def configure(self, coin, entry_price, take_profit, trailing_gap, capital):
        self.coin = coin.upper()
        self.entry_price = float(entry_price)
        self.take_profit = float(take_profit)
        self.trailing_gap = float(trailing_gap)
        self.capital = float(capital)
        self.state = BotState.WAIT_ENTRY

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        self.state = BotState.PAUSED

    def loop(self):
        while self.running:
            try:
                if self.state == BotState.WAIT_ENTRY:
                    entry_engine.run(self)
                elif self.state == BotState.BUYING:
                    buy_engine.run(self)
                elif self.state == BotState.VERIFY_BUY:
                    verify_buy_engine.run(self)
                elif self.state == BotState.HOLDING:
                    holding_engine.run(self)
                elif self.state == BotState.TP_ZONE:
                    tp_engine.run(self)
                elif self.state == BotState.TRAILING:
                    trailing_engine.run(self)
                elif self.state == BotState.SELLING:
                    sell_engine.run(self)
                elif self.state == BotState.VERIFY_SELL:
                    verify_sell_engine.run(self)
                elif self.state == BotState.FINISHED:
                    finish_engine.run(self)
            except Exception as e:
                print(e)
            time.sleep(self.interval)

    def get_status(self):

        return {

            "status": "RUNNING" if self.running else "STOPPED",

            "state": self.state.value,

            "coin": self.coin,

            "entry_price": self.entry_price,

            "buy_price": self.buy_price,

            "sell_price": self.sell_price,

            "current_price": self.current_price,

            "highest_price": self.highest_price,

            "qty": self.qty,

            "capital": self.capital,

            "take_profit": self.take_profit,

            "trailing_gap": self.trailing_gap

        }
    def restore_position(self, position):
        self.coin = position["coin"]
        self.buy_price = position["buy_price"]
        self.entry_price = position["buy_price"]
        self.capital = position["capital"]
        self.qty = position.get("qty",0)
        self.highest_price = position.get("highest_price", self.buy_price)
        self.current_price = self.buy_price
        self.state = BotState.HOLDING

engine = ExecutionEngine()
