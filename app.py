from flask import Flask
from api.indodax import api
import os
import json
from datetime import datetime

import config

app = Flask(__name__)


FILES = [
    "config.json",
    "active_trades.json",
    "history.json",
    "bot_state.json"
]


def init_storage():
    os.makedirs(config.DATA_DIR, exist_ok=True)

    defaults = {
        "config.json": {},
        "active_trades.json": [],
        "history.json": [],
        "bot_state.json": {
            "status": "RUNNING",
            "engine": "IDLE",
            "version": config.VERSION,
            "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }

    for file in FILES:
        path = os.path.join(config.DATA_DIR, file)

        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump(defaults[file], f, indent=4)


init_storage()

@app.route("/")
def home():

    btc = api.get_ticker("btcidr")

    if btc["success"]:

        price = f"{btc['last']:,.0f}"

        status = "Connected"

    else:

        price = "-"

        status = btc["error"]

    return f"""
    <h2>{config.APP_NAME}</h2>

    <p>Version : {config.VERSION}</p>

    <p>Status : Running</p>

    <p>API : {status}</p>

    <p>BTC : Rp {price}</p>

    <p>Engine : Idle</p>
    """

if __name__ == "__main__":
    app.run(
        host=config.HOST,
        port=config.PORT
    )
