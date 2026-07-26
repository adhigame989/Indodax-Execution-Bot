from flask import Flask, render_template
from flask import request, redirect
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
from api.private import private
from core.wallet_manager import wallet
from flask import jsonify

app = Flask(__name__)

FILES = [
    "config.json",
    "active_trades.json",
    "history.json",
    "bot_state.json"
]

def format_rupiah(value):

    try:
        return f"Rp {float(value):,.0f}".replace(",", ".")

    except:

        return "Rp -"
        
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

    status = engine.get_status()
    buy = float(status.get("buy_price", 0) or 0)
    current = float(status.get("current_price", 0) or 0)
    qty = float(status.get("qty", 0) or 0)

    if buy > 0 and current > 0:

        pnl_percent = ((current - buy) / buy) * 100

        pnl_value = (current - buy) * qty

    else:

        pnl_percent = 0

        pnl_value = 0

    if status.get("coin"):
        status["coin"] = status["coin"].replace("_IDR", "")

    status["entry_price"] = format_rupiah(status.get("entry_price", 0))
    status["buy_price"] = format_rupiah(status.get("buy_price", 0))
    status["sell_price"] = format_rupiah(status.get("sell_price", 0))
    status["current_price"] = format_rupiah(status.get("current_price", 0))
    status["capital"] = format_rupiah(status.get("capital", 0))
    
    wallet = {

        "idr": 0,

        "coin": 0,

        "equity": 0

        }

    hold_time = "-"

    if engine.buy_time:

        delta = datetime.now() - engine.buy_time

        total = int(delta.total_seconds())

        hours = total // 3600

        minutes = (total % 3600) // 60

        hold_time = f"{hours}h {minutes}m"
        
    position = {

        "active": status.get("state") in [
            "HOLDING",
            "TP_ZONE",
            "TRAILING",
            "SELLING"
        ],

        "coin": status.get("coin", "-"),

        "capital": status.get("capital", "Rp -"),

        "qty": status.get("qty", 0),

        "buy_price": status.get("buy_price", "Rp -"),

        "current_price": status.get("current_price", "Rp -"),

        "highest": format_rupiah(
            status.get("highest_price", 0)
        ),

        "pnl_percent": f"{pnl_percent:+.2f}%",

        "pnl": format_rupiah(pnl_value),

        "hold_time": hold_time

        }
    
    cfg = config_manager.load()
    config_data = {

        "coin": cfg.get("coin"),

        "entry_price": format_rupiah(
            cfg.get("entry_price",0)
        ),

        "entry_price_raw": cfg.get("entry_price",0),

        "capital": format_rupiah(
            cfg.get("capital",0)
        ),

        "capital_raw": cfg.get("capital",0),

        "take_profit": cfg.get("tp_zone",[0])[0],

        "trailing_gap": cfg.get("trailing_gap",0),

        "interval":60

        }
    
    return render_template(
        "index.html",
        app_name=config.APP_NAME,
        version=config.VERSION,
        api_status=api_status,
        btc=btc,
        engine=status,
        wallet=wallet,
        position=position,
        config_data=config_data,
        bot_status=status.get("status","RUNNING")
    )

@app.route("/save_config", methods=["POST"])
def save_config():

    cfg = config_manager.load()

    cfg.setdefault("running", True)

    cfg["coin"] = request.form["coin"]

    cfg["entry_price"] = int(request.form["entry_price"])

    cfg["capital"] = int(request.form["capital"])

    cfg["tp_zone"][0] = int(request.form["tp"])

    cfg["trailing_gap"] = int(request.form["trailing_gap"])

    config_manager.save(cfg)
   
    engine.configure(
        coin=cfg["coin"],
        entry_price=cfg["entry_price"],
        take_profit=cfg["tp_zone"][0],
        trailing_gap=cfg["trailing_gap"],
        capital=cfg["capital"]
        )

    return redirect("/")
    
@app.post("/bot/start")
def start_bot():

    cfg = config_manager.set_running(True)

    engine.configure(
        coin=cfg["coin"],
        entry_price=cfg["entry_price"],
        take_profit=cfg["tp_zone"][0],
        trailing_gap=cfg["trailing_gap"],
        capital=cfg["capital"]
    )

    engine.start()

    return redirect("/")
@app.post("/bot/stop")
def stop_bot():

    config_manager.set_running(False)

    engine.stop()

    return redirect("/")
    
@app.post("/config/default")
def load_default():

    cfg = config_manager.load_default()

    engine.configure(
        coin=cfg["coin"],
        entry_price=cfg["entry_price"],
        take_profit=cfg["tp_zone"][0],
        trailing_gap=cfg["trailing_gap"],
        capital=cfg["capital"]
    )

    return redirect("/")

@app.get("/api/validate_coin")
def validate_coin():

    coin = request.args.get("coin", "").upper().strip()

    if not coin:
        return jsonify({
            "valid": False,
            "price": None
        })

    try:

        ticker = api.get_ticker()

        pair = coin.lower()

        if pair not in ticker["tickers"]:

            return jsonify({
                "valid": False,
                "price": None
            })

        data = ticker["tickers"][pair]

        return jsonify({

            "valid": True,

            "price": int(float(data["last"]))

        })

    except Exception:

        return jsonify({

            "valid": False,

            "price": None

        })
    
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

@app.route("/api/wallet")
def api_wallet():

    return private.get_info()

@app.route("/api/balance")
def api_balance():

    return {

        "idr": wallet.get_idr_balance(),

        "btc": wallet.get_coin_balance("btc")
    }

@app.route("/api/config")
def api_config():

    return config_manager.load()
    
if __name__ == "__main__":

    app.run(
        host=config.HOST,
        port=config.PORT
    )
