from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler

class UserFeedBackHandler(BaseHandler):
    @coroutine
    def post(self):
        token = self.get_json_argument("token")
        info = self.get_json_argument("info")
        cur = yield self.db.execute(#ensure the user exists
        "SELECT * FROM customer WHERE token=%s",
            (
            token
            )
        )
        if cur.rowcount != 0:
            user = cur.fetchone()
            tel_phone = user["tel_phone"]
            yield self.db.execute("insert into user_feed_back (info,tel_phone) values(%s,%s)",
                (
                info,
                tel_phone,
                )
            )
            state = {'feed_back':'success'}
            self.fin_succ(**state)
        else:
            state = {'feed_back':'token_error'}
            self.fin_succ(**state)
