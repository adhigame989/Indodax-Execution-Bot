from flask import Flask, render_template
import os
import json
from datetime import datetime

import config

from api.indodax import api
from engine.monitor import monitor
from engine.execution import engine

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

monitor.start()

engine.configure(
    coin="BTC_IDR",
    entry_price=1700000000,
    take_profit=3,
    trailing_gap=1,
    capital=100000
)

engine.start()


@app.route("/")
def home():

    btc = api.get_ticker("btc_idr")

    if btc:

        api_status = "Connected"

        btc = {
            "last": f"{btc['last']:,.0f}",
            "buy": f"{btc['buy']:,.0f}",
            "sell": f"{btc['sell']:,.0f}"
        }

    else:

        api_status = "Disconnected"

        btc = {
            "last": "-",
            "buy": "-",
            "sell": "-"
        }

    return render_template(
        "index.html",
        app_name=config.APP_NAME,
        version=config.VERSION,
        api_status=api_status,
        btc=btc,
        engine=engine.get_status()
    )


@app.route("/health")
def health():

    return {
        "status": "ok",
        "version": config.VERSION
    }


if __name__ == "__main__":

    app.run(
        host=config.HOST,
        port=config.PORT
    )
