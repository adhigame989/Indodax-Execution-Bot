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


config_manager = ConfigManager()
