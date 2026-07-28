from api.private import private


class OrderEngine:

    def buy(self, pair, price, capital):

        result = private.buy(
            pair=pair,
            price=price,
            idr=capital
        )

        if result.get("success") != 1:
            return {
                "success": False,
                "message": result.get("error", "BUY FAILED")
            }

        return {
            "success": True,
            "order_id": result["return"]["order_id"],
            "message": "BUY ORDER CREATED"
        }

    def sell(self, pair, price, qty):

        result = private.sell(
            pair=pair,
            price=price,
            coin=qty
        )

        if result.get("success") != 1:
            return {
                "success": False,
                "message": result.get("error", "SELL FAILED")
            }

        return {
            "success": True,
            "order_id": result["return"]["order_id"],
            "message": "SELL ORDER CREATED"
        }

    def verify_buy(self, pair, order_id):

        result = private.get_order(pair, order_id)

        if result.get("success") != 1:
            return {
                "success": False,
                "filled": False,
                "message": result.get("error", "VERIFY FAILED")
            }

        data = result.get("return", {})

        order = data.get("buy")

        if order is None:
            order = data.get("order", {})

        if not order:
            return {
                "success": True,
                "filled": False
            }

        status = str(order.get("status", "")).lower()

        if status != "filled":
            return {
                "success": True,
                "filled": False
            }

        coin = pair.lower().replace("_idr", "")

        qty = 0

        receive_key = f"receive_{coin}"

        if receive_key in order:
            qty = float(order.get(receive_key, 0))

        elif "order_amount" in order:
            qty = float(order.get("order_amount", 0))

        elif "receive_coin" in order:
            qty = float(order.get("receive_coin", 0))

        return {
            "success": True,
            "filled": True,
            "price": float(order.get("price", 0)),
            "qty": qty
        }

    def verify_sell(self, pair, order_id):

        result = private.get_order(pair, order_id)

        if result.get("success") != 1:
            return {
                "success": False,
                "filled": False,
                "message": result.get("error", "VERIFY FAILED")
            }

        data = result.get("return", {})

        sell = data.get("sell")

        if sell is None:
            sell = data.get("order", {})

        if not sell:
            return {
                "success": True,
                "filled": False
            }

        status = str(sell.get("status", "")).lower()

        if status != "filled":
            return {
                "success": True,
                "filled": False
            }

        return {
            "success": True,
            "filled": True,
            "price": float(sell.get("price", 0))
        }

    def cancel(self, pair, order_id, order_type):

        result = private.cancel_order(
            pair,
            order_id,
            order_type
        )

        if result.get("success") != 1:
            return {
                "success": False,
                "message": result.get("error", "CANCEL FAILED")
            }

        return {
            "success": True
        }


order = OrderEngine()
