from api.private import private


class OrderEngine:

    # ==========================
    # BUY
    # ==========================

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

        data = result["return"]

        return {
            "success": True,
            "order_id": data["order_id"],
            "message": "BUY ORDER CREATED"
        }

    # ==========================
    # SELL
    # ==========================

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

        data = result["return"]

        return {
            "success": True,
            "order_id": data["order_id"],
            "message": "SELL ORDER CREATED"
        }

    # ==========================
    # VERIFY BUY
    # ==========================

    def verify_buy(self, pair, order_id):

        result = private.get_order(
            pair,
            order_id
        )
        print("VERIFY RESPONSE:")
        print(result)

        if result.get("success") != 1:

            return {
                "success": False,
                "filled": False,
                "message": result.get("error", "VERIFY FAILED")
            }

        data = result["return"]

        buy = data.get("buy", {})

        status = buy.get("status", "")

        print("=" * 50)
        print("VERIFY BUY DEBUG")
        print("BUY OBJECT :", buy)
        print("STATUS     :", status)
        print("PRICE      :", buy.get("price"))
        print("ORDER_AMT  :", buy.get("order_amount"))
        print("REMAIN_RP  :", buy.get("remain_rp"))
        print("REFUND     :", buy.get("refund"))
        print("=" * 50)

        if status.lower() == "filled":

            return {
                "success": True,
                "filled": True,
                "price": float(buy.get("price", 0)),
                "qty": float(buy.get("order_amount", 0))
            }

        return {
            "success": True,
            "filled": False
        }

    # ==========================
    # VERIFY SELL
    # ==========================

    def verify_sell(self, pair, order_id):

        result = private.get_order(
            pair,
            order_id
        )

        if result.get("success") != 1:

            return {
                "success": False,
                "filled": False,
                "message": result.get("error", "VERIFY FAILED")
            }

        data = result["return"]

        sell = data.get("sell", {})

        status = sell.get("status", "")

        if status.lower() == "filled":

            return {
                "success": True,
                "filled": True,
                "price": float(sell.get("price", 0))
            }

        return {
            "success": True,
            "filled": False
        }

    # ==========================
    # CANCEL
    # ==========================

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
