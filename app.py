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

    api.update()

    btc = api.get_ticker("btcidr")

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

    </body>

    </html>
    """

if __name__ == "__main__":
    app.run(
        host=config.HOST,
        port=config.PORT
    )
