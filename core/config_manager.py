import json
import os
import config


class ConfigManager:

    def __init__(self):

        self.file = os.path.join(
            config.DATA_DIR,
            "config.json"
        )

    def load(self):

        with open(self.file, "r") as f:

            return json.load(f)

    def save(self, data):

        with open(self.file, "w") as f:

            json.dump(data, f, indent=4)

    def set_running(self, running):

        cfg = self.load()

        cfg["running"] = running

        self.save(cfg)

        return cfg


    def load_default(self):

        cfg = self.load()

        cfg["coin"] = "BTC_IDR"
        cfg["entry_price"] = 0
        cfg["capital"] = 100000
        cfg["tp_zone"] = [3]
        cfg["trailing_gap"] = 1
        cfg["running"] = False

        self.save(cfg)

        return cfg


config_manager = ConfigManager()
