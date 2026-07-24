import json
import os
from datetime import datetime

import config


class PositionManager:

    def __init__(self):

        self.file = os.path.join(
            config.DATA_DIR,
            "active_trades.json"
        )

    def load(self):

        if not os.path.exists(self.file):

            return []

        with open(self.file, "r") as f:

            return json.load(f)

    def save(self, positions):

        with open(self.file, "w") as f:

            json.dump(
                positions,
                f,
                indent=4
            )

    def add(self,
            coin,
            buy_price,
            capital,
            qty):

        positions = self.load()

        position = {

            "coin": coin,

            "buy_price": buy_price,

            "capital": capital,

            "qty": qty,

            "highest_price": buy_price,

            "state": "HOLDING",

            "buy_time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        }

        positions.append(position)

        self.save(positions)

        return position

    def remove(self, coin):

        positions = self.load()

        positions = [

            p for p in positions

            if p["coin"] != coin

        ]

        self.save(positions)

    def get(self, coin):

        positions = self.load()

        for p in positions:

            if p["coin"] == coin:

                return p

        return None

    def get_all(self):

        return self.load()
        
    def update_highest(
            self,
            coin,
            highest_price):

        positions = self.load()

        for p in positions:

            if p["coin"] == coin:

                p["highest_price"] = highest_price

        self.save(positions)


position_manager = PositionManager()
