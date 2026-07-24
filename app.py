from flask import Flask, render_template
import os
import json
from datetime import datetime

import config

from api.indodax import api
from engine.monitor import monitor
from engine.execution import engine
from core.config_manager import config_manager
from core.position_manager import position_manager
from engine.recovery import recovery

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

cfg = config_manager.load()

engine.configure(

    coin=cfg["coin"],

    entry_price=cfg["entry_price"],

    take_profit=cfg["tp_zone"][0],

    trailing_gap=cfg["trailing_gap"],

    capital=cfg["capital"]

)

if not recovery.restore(engine):

    cfg = config_manager.load()

    engine.configure(

        coin=cfg["coin"],

        entry_price=cfg["entry_price"],

        take_profit=cfg["tp_zone"][0],

        trailing_gap=cfg["trailing_gap"],

        capital=cfg["capital"]

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

@app.route("/api/status")
def api_status():

    btc = api.get_ticker("btc_idr")

    if btc is None:

        btc = {
            "last": 0,
            "buy": 0,
            "sell": 0
        }

    return {

        "bot": {

            "name": config.APP_NAME,

            "version": config.VERSION

        },

        "market": btc,

        "engine": engine.get_status()

    }

@app.route("/api/config")
def api_config():

    return config_manager.load()
    
if __name__ == "__main__":

    app.run(
        host=config.HOST,
        port=config.PORT
    )
