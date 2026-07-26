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
        config = self.load()

        config["running"] = running

        self.save(config)

        return config


config_manager = ConfigManager()
