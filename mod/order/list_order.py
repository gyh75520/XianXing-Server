from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
from mod.base.json_encoder import MyEncoder
from datetime import date, datetime
import json
from mod.base.exceptions import ArgsError, PermissionDeniedError,OtherError

class ListOrderHandler(BaseHandler):
    @coroutine
    def post(self):
        token = self.get_json_argument("token")

        cur = yield self.db.execute(#ensure the user exists
        "SELECT * FROM customer WHERE token=%s",
            (
            token
            )
        )
        if cur.rowcount != 0:
            user = cur.fetchone()
            tel_phone = user["tel_phone"]
            curorder = yield self.db.execute(
            "SELECT cha_phone,market_name,start_time,all_price,ostatus,order_num,m.url as url FROM user_order u ,market m WHERE u.tel_phone=%s and m.market_id=u.market_id order by start_time DESC",
                (
                tel_phone,
                )
            )
            order=curorder.fetchall()	
            orders = {'order':order}
            state =json.dumps(orders, cls=MyEncoder)
            self.finish(state)
        else:
            state = {'order':'token_error'}
            self.fin_succ(**state)
