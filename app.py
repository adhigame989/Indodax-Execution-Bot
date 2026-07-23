from flask import Flask
from api.indodax import api
from engine.monitor import monitor
from engine.execution import engine
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

        status = "Connected"

        price = f"{btc['last']:,.0f}"
        buy = f"{btc['buy']:,.0f}"
        sell = f"{btc['sell']:,.0f}"

    else:

        status = "Disconnected"

        price = "-"
        buy = "-"
        sell = "-"

    return f"""
    <html>

    <head>

        <meta http-equiv="refresh" content="2">

        <title>{config.APP_NAME}</title>

    </head>

    <body>

        <h2>{config.APP_NAME}</h2>

        <p><b>Version :</b> {config.VERSION}</p>

        <p><b>Status :</b> Running</p>

        <p><b>API :</b> {status}</p>

        <hr>

        <h3>BTC/IDR</h3>

        <p>Last : Rp {price}</p>

        <p>Buy : Rp {buy}</p>

        <p>Sell : Rp {sell}</p>

        <hr>

        <p>Engine : Idle</p>

        <hr>

        <h3>Execution Engine</h3>

        <p>State : {engine.get_status()['state']}</p>

        <p>Coin : {engine.get_status()['coin']}</p>
        
        <p>Entry : Rp {engine.get_status()['entry_price']:,.0f}</p>
        
        <p>TP : {engine.get_status()['take_profit']} %</p>
        
        <p>Trailing : {engine.get_status()['trailing_gap']} %</p>
        
        <p>Capital : Rp {engine.get_status()['capital']:,.0f}</p>

    </body>

    </html>
    """

if __name__ == "__main__":
    app.run(
        host=config.HOST,
        port=config.PORT
    )
