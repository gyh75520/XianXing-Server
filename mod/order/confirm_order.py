from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler

class ConfirmOrderHandler(BaseHandler):
    @coroutine
    def post(self):
        token = self.get_json_argument("token")
        order_num = self.get_json_argument("order_num")
        rec_time = self.get_json_argument("rec_time")
        cur = yield self.db.execute(#ensure the user exists
        "SELECT * FROM customer WHERE token=%s",
            (
            token
            )
        )
        if cur.rowcount != 0:
            curorder = yield self.db.execute(
            "SELECT * FROM user_order WHERE order_num=%s and ostatus=2",
                (
                order_num,
                )
            )
            if curorder.rowcount != 0:
                yield self.db.execute("update user_order set ostatus=3,rec_time=%s where order_num=%s",
                    (
                    rec_time,
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
