from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
from mod.base.json_encoder import MyEncoder
import json

class OrderStatueHandler(BaseHandler):
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
            "SELECT jd_time,ostatus,rec_time,remark_time FROM user_order WHERE order_num=%s",
                (
                order_num,
                )
            )
            if curorder.rowcount != 0:
                order=curorder.fetchone()
                orders = {'order':order}
                state =json.dumps(orders, cls=MyEncoder)
                self.finish(state)
            else:
                state = {'order':'order_num_error'}
                self.fin_succ(**state)
        else:
            state = {'order':'token_error'}
            self.fin_succ(**state)
