from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler

class EvaluateOrderHandler(BaseHandler):
    @coroutine
    def post(self):
        token = self.get_json_argument("token")
        order_num = self.get_json_argument("order_num")
        remark_time = self.get_json_argument("remark_time")
        remark_score = self.get_json_argument("remark_score")
        remark = self.get_json_argument("remark")
        cur = yield self.db.execute(#ensure the user exists
        "SELECT * FROM customer WHERE token=%s",
            (
            token
            )
        )
        if cur.rowcount != 0:
            curorder = yield self.db.execute(
            "SELECT * FROM user_order WHERE order_num=%s and ostatus>2",
                (
                order_num,
                )
            )
            if curorder.rowcount != 0:
                yield self.db.execute("update user_order set ostatus=4,remark_time=%s,remark_score=%s,remark=%s where order_num=%s",
                    (
                    remark_time,
                    remark_score,
                    remark,
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
