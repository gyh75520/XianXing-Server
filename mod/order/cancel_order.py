from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler

class CancelOrderHandler(BaseHandler):
    @coroutine
    def post(self):
        token = self.get_json_argument("token")
        order_num = self.get_json_argument("order_num")

        cur = yield self.db.execute(#ensure the user exists
        "SELECT * FROM customer WHERE token=%s",
            (
            token
            )
        )
        if cur.rowcount != 0:
            curorder = yield self.db.execute(
            "SELECT order_id FROM user_order WHERE order_num=%s and ostatus=1",
                (
                order_num,
                )
            )
            if curorder.rowcount != 0:
                order = curorder.fetchone()
                order_id=order["order_id"]
                curfood = yield self.db.execute(
                "select food_id,amount from food_amount where order_id=%s",
                    (
                    order_id
                    )
                )
                foods = curfood.fetchall()
                for food in foods:
                    amount=food["amount"]
                    food_id=food["food_id"]
                    yield self.db.execute(
                    "UPDATE food SET surplus=surplus+%s WHERE food_id=%s",
                        (
                        amount, 
                        food_id,
                        )
                    )

                yield self.db.execute(
                "DELETE FROM food_amount WHERE order_id=%s",
                    (
                    order_id,
                    )
                )
                yield self.db.execute(
                "DELETE FROM user_order WHERE order_num=%s",
                    (
                    order_num,
                    )
                )
                state = {'order':'success'}
                self.fin_succ(**state) 
            else:
                state = {'order':'order_num_error'}
                self.fin_succ(**state)
        else:
            state = {'order':'token_error'}
            self.fin_succ(**state)
