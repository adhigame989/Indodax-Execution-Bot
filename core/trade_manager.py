import os
import json
from datetime import datetime
import config


class TradeManager:

    def __init__(self):

        self.file = os.path.join(
            config.DATA_DIR,
            "trade_setups.json"
        )

        if not os.path.exists(self.file):

            with open(self.file, "w") as f:

                json.dump([], f, indent=4)

    def load(self):

        try:

            with open(self.file, "r") as f:

                return json.load(f)

        except:

            return []

    def save(self, trades):

        with open(self.file, "w") as f:

            json.dump(
                trades,
                f,
                indent=4
            )

    def next_id(self):

        trades = self.load()

        if not trades:

            return 1

        return max(
            t["id"] for t in trades
        ) + 1

    def create_trade(
        self,
        coin,
        capital,
        entry_price,
        target_price,
        trailing_gap
    ):

        trades = self.load()

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        trade = {

            "id": self.next_id(),

            "state": "WAIT_ENTRY",

            "coin": coin.upper(),

            "capital": capital,

            "entry_price": entry_price,

            "target_price": target_price,

            "trailing_gap": trailing_gap,

            "buy_price": 0,

            "qty": 0,

            "highest_price": 0,

            "current_price": 0,

            "current_value": 0,

            "profit_percent": 0,

            "profit_value": 0,

            "buy_time": None,

            "sell_time": None,

            "created_at": now,

            "updated_at": now

        }

        trades.append(trade)

        self.save(trades)

        return trade

    def get_all(self):

        return self.load()

    def get_trade(
        self,
        trade_id
    ):

        for trade in self.load():

            if trade["id"] == trade_id:

                return trade

        return None

    def update_trade(
        self,
        trade_id,
        **kwargs
    ):

        trades = self.load()

        for trade in trades:

            if trade["id"] == trade_id:

                trade.update(kwargs)

                trade["updated_at"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                break

        self.save(trades)

    def delete_trade(
        self,
        trade_id
    ):

        trades = [

            t

            for t in self.load()

            if t["id"] != trade_id

        ]

        self.save(trades)


trade_manager = TradeManager()
