import threading
import time

from engine.state import BotState
from engine.order import order
from core.position_manager import position_manager


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

        self.highest_price = 0

        self.current_price = 0

        self.trailing_price = 0

        self.tp_activated = False

        self.order_id = None

        self.sell_order_id = None

        self.last_buy_failed = 0

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

        from api.indodax import api

        while self.running:

            if self.state == BotState.WAIT_ENTRY:

                ticker = api.get_ticker(self.coin)

                if ticker:

                    self.current_price = ticker["last"]

                    print(
                        f"[{self.coin}] "
                        f"Current: {self.current_price:,.0f} | "
                        f"Entry: {self.entry_price:,.0f}"
                    )

                    if self.current_price <= self.entry_price:

                        now = time.time()

                        if now - self.last_buy_failed < config.BUY_RETRY_DELAY:

                            remain = int(
                                config.BUY_RETRY_DELAY -
                                (now - self.last_buy_failed))

                            print(f"BUY COOLDOWN ({remain}s)")

                            return

                        print("ENTRY TRIGGERED")

                        self.state = BotState.BUYING
            elif self.state == BotState.BUYING:

                result = order.buy(

                    self.coin,

                    self.entry_price,

                    self.capital
                )
                
                if result["success"]:

                    self.order_id = result["order_id"]

                    print(f"BUY ORDER CREATED : {self.order_id}")

                    self.state = BotState.VERIFY_BUY

                else:
                    
                    self.last_buy_failed = time.time()

                    print(result["message"])
                    
                    print(f"Retry Buy in {config.BUY_RETRY_DELAY}s")

                    self.state = BotState.WAIT_ENTRY

            elif self.state == BotState.VERIFY_BUY:

                verify = order.verify_buy(

                    self.coin,

                    self.order_id

                )

                if verify["success"] and verify["filled"]:

                    self.buy_price = verify["price"]

                    self.highest_price = verify["price"]

                    qty = verify["qty"]

                    position_manager.add(

                        coin=self.coin,

                        buy_price=self.buy_price,

                        capital=self.capital,

                        qty=qty

                    )

                    print("BUY VERIFIED")

                    self.state = BotState.HOLDING

                elif verify["success"]:

                    print("WAIT BUY FILL")

                else:

                    print(verify.get("message", "VERIFY FAILED"))
                    
            elif self.state == BotState.HOLDING:

                ticker = api.get_ticker(self.coin)

                if ticker:

                    self.current_price = ticker["last"]

                    if self.current_price > self.highest_price:

                        self.highest_price = self.current_price

                        position_manager.update_highest(self.coin,self.highest_price)

                    profit = (
                        (self.current_price - self.buy_price)
                        / self.buy_price) * 100

                    print(
                        f"HOLDING | "
                        f"Price={self.current_price:,.0f} | "
                        f"Profit={profit:.2f}%"
                    )

                    if profit >= self.take_profit:

                        print("TP ZONE REACHED")

                        self.state = BotState.TP_ZONE

            elif self.state == BotState.TP_ZONE:

                ticker = api.get_ticker(self.coin)

                if ticker:

                    self.current_price = ticker["last"]

                    if self.current_price > self.highest_price:

                        self.highest_price = self.current_price

                    self.trailing_price = self.highest_price * (
                        1 - self.trailing_gap / 100
                    )

                    print(
                        f"Highest={self.highest_price:,.0f}"
                    )

                    print(
                        f"Trailing={self.trailing_price:,.0f}"
                    )

                    if self.current_price <= self.trailing_price:

                        print("TRAILING HIT")

                        self.state = BotState.SELLING

            elif self.state == BotState.SELLING:

                qty = self.capital / self.buy_price

                result = order.sell(

                    self.coin,

                    self.current_price,

                    qty

                )

                if result["success"]:

                    self.sell_order_id = result["order_id"]

                    self.state = BotState.VERIFY_SELL

                else:

                    print(result["message"])

            elif self.state == BotState.VERIFY_SELL:

                verify = order.verify_sell(

                    self.coin,

                    self.sell_order_id

                )

                if verify["success"] and verify["filled"]:

                    position_manager.remove(self.coin)

                    print("SELL VERIFIED")

                    self.state = BotState.FINISHED

                elif verify["success"]:

                    print("WAIT SELL FILL")

                else:

                    print(verify.get("message", "VERIFY FAILED"))
            
            elif self.state == BotState.FINISHED:

                print("TRADE FINISHED")

                self.running = False
            
            time.sleep(self.interval)

    def get_status(self):

        return {

            "state": self.state.value,

            "coin": self.coin,

            "entry_price": self.entry_price,

            "take_profit": self.take_profit,

            "trailing_gap": self.trailing_gap,

            "capital": self.capital,

            "buy_price": self.buy_price,

            "highest_price": self.highest_price,

        }
    def restore_position(self, position):

        print("=" * 40)
        print("RESTORE POSITION")
        print("=" * 40)

        self.coin = position["coin"]

        self.buy_price = position["buy_price"]

        self.entry_price = position["buy_price"]

        self.capital = position["capital"]

        self.highest_price = position["highest_price"]

        self.state = BotState.HOLDING

        print(f"Coin : {self.coin}")
 
        print(f"Buy  : {self.buy_price}")

        print("RESTORE SUCCESS")


engine = ExecutionEngine()
