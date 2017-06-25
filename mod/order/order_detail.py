from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
from mod.base.json_encoder import MyEncoder
import json

class OrderDetailHandler(BaseHandler):
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
            "SELECT del_time,user_name,sex,pay_way,get_way,rec_phone,address,del_pri,PS,order_id FROM user_order WHERE order_num=%s",
                (
                order_num,
                )
            )
            if curorder.rowcount != 0:
                order=curorder.fetchone()
                order_id=order["order_id"]
                curfood = yield self.db.execute(
                "select food_name as name,spec,unit_price as price,amount,url from food_amount fm ,food f where fm.food_id=f.food_id and fm.order_id=%s",
                    (
                    order_id,
                    )
                )
                food=curfood.fetchall()
                order["goods"]=food
                del order["order_id"]
                orders = {'order':order}
                state =json.dumps(orders, cls=MyEncoder)
                self.finish(state)
            else:
                state = {'order':'order_num_error'}
                self.fin_succ(**state)
        else:
            state = {'order':'token_error'}
            self.fin_succ(**state)
