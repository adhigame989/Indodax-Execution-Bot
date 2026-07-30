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
from core.wallet_manager import wallet as wallet_manager
from flask import jsonify
from core.trade_manager import trade_manager

app = Flask(__name__)

FILES = [
    "config.json",
    "active_trades.json",
    "history.json",
    "bot_state.json",
    "trade_setups.json"
]

def format_rupiah(value):

    try:
        return f"Rp {float(value):,.0f}".replace(",", ".")

    except:

        return "Rp -"
        
def init_storage():

    os.makedirs(config.DATA_DIR, exist_ok=True)

    defaults = {
        "config.json": {
            "coin": "BTC_IDR",
            "capital": 100000,
            "entry_price": 0,
            "target_price": 0,
            "trailing_gap": 1,
            "running": True
        },
        "active_trades.json": [],
        "history.json": [],
        "trade_setups.json": [],
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

api.update()

monitor.start()

def get_next_trade():
    trades = trade_manager.get_all()

    for trade in trades:
        if trade.get("state") == "WAIT_ENTRY":
            return trade

    return None
    
if not recovery.restore(engine):

    trade = get_next_trade()

    if trade:

        engine.configure(
            coin=trade["coin"],
            entry_price=trade["entry_price"],
            target_price=trade["target_price"],
            trailing_gap=trade["trailing_gap"],
            capital=trade["capital"],
            trade_id=trade["id"]
        )

    else:

        cfg = config_manager.load()

        engine.configure(
            coin=cfg.get("coin", "BTC_IDR"),
            entry_price=0,
            target_price=0,
            trailing_gap=1,
            capital=0
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
    
    trade = get_next_trade()

    coin = trade["coin"] if trade else "BTC_IDR"

    wallet = wallet_manager.get_wallet_summary(coin)
 
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
    
    
    if trade:

        config_data = {
            "coin": trade["coin"],
            "capital": format_rupiah(trade["capital"]),
            "capital_raw": trade["capital"],
            "entry_price": format_rupiah(trade["entry_price"]),
            "entry_price_raw": trade["entry_price"],
            "target_price": format_rupiah(trade["target_price"]),
            "target_price_raw": trade["target_price"],
            "trailing_gap": trade["trailing_gap"]
        }

    else:

        config_data = {
            "coin": "-",
            "capital": "Rp -",
            "capital_raw": 0,
            "entry_price": "Rp -",
            "entry_price_raw": 0,
            "target_price": "Rp -",
            "target_price_raw": 0,
            "trailing_gap": 0
        }

    trade_setups = trade_manager.get_all()

    waiting_count = 0
    active_count = 0

    for trade in trade_setups:

        state = trade.get("state", "WAIT_ENTRY")

        if state == "WAIT_ENTRY":
            waiting_count += 1

        elif state in [
            "BUYING",
            "VERIFY_BUY",
            "HOLDING",
            "TP_ZONE",
            "TRAILING",
            "SELLING"
        ]:
            active_count += 1
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
        trade_setups=trade_setups,
        waiting_count=waiting_count,
        active_count=active_count,
        queue_count=len(trade_setups),
        bot_status=status.get("status","RUNNING")
    )

@app.route("/create_trade", methods=["POST"])
def create_trade():

    print("========== CREATE TRADE ==========")
    print(request.method)
    print(dict(request.form))
    
    trade_manager.create_trade(

        coin=request.form["coin"],

        capital=int(request.form["capital"]),

        entry_price=int(request.form["entry_price"]),

        target_price=int(request.form["target_price"]),

        trailing_gap=int(request.form["trailing_gap"])

    )

    print(trade_manager.get_all())
    return redirect("/")
    
@app.post("/bot/start")
def start_bot():

    config_manager.set_running(True)

    trade = get_next_trade()

    if trade:

        engine.configure(
            coin=trade["coin"],
            entry_price=trade["entry_price"],
            target_price=trade["target_price"],
            trailing_gap=trade["trailing_gap"],
            capital=trade["capital"],
            trade_id=trade["id"]
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
        target_price=cfg["target_price"],
        trailing_gap=cfg["trailing_gap"],
        capital=cfg["capital"],
    )

    return redirect("/")

@app.get("/api/validate_coin")
def validate_coin():

    coin = request.args.get("coin", "").strip().lower()

    if not coin:
        return jsonify({
            "valid": False,
            "price": None
        })

    try:

        ticker = api.get_ticker(coin)

        if ticker is None:

            return jsonify({
                "valid": False,
                "price": None
            })

        return jsonify({

            "valid": True,

            "price": ticker["last"]

        })

    except Exception as e:

        print(e)

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

        "idr": wallet_manager.get_idr_balance(),

        "btc": wallet_manager.get_coin_balance("btc")
    }

@app.route("/api/config")
def api_config():

    trade = get_next_trade()

    if trade:
        return trade

    return {}

@app.route("/edit_trade/<int:trade_id>")
def edit_trade(trade_id):

    trade = trade_manager.get_trade(trade_id)

    if not trade:
        return redirect("/")

    return render_template(
        "edit_trade.html",
        trade=trade
    )

@app.route("/update_trade/<int:trade_id>", methods=["POST"])
def update_trade(trade_id):

    trade_manager.update_trade(
        trade_id,
        coin=request.form["coin"].upper(),
        capital=int(request.form["capital"]),
        entry_price=int(request.form["entry_price"]),
        target_price=int(request.form["target_price"]),
        trailing_gap=float(request.form["trailing_gap"])
    )

    return redirect("/")

@app.route("/delete_trade/<int:trade_id>")
def delete_trade(trade_id):

    trade_manager.delete_trade(trade_id)

    return redirect("/")
    
if __name__ == "__main__":

    app.run(
        host=config.HOST,
        port=config.PORT
    )
