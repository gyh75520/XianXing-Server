from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
import time
from mod.base.exceptions import ArgsError, PermissionDeniedError,OtherError

class ReLoginHandler(BaseHandler):
    @coroutine
    def post(self):
        token = self.get_json_argument("token")
        cur = yield self.db.execute(
            "SELECT tel_phone,nick_name,token FROM customer WHERE token=%s",
            (
                token
            )
        )
        if cur.rowcount != 0:
            yield self.db.execute(
            "UPDATE customer SET last_log=%s WHERE token=%s",
                (
                time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),
                token,
                )
            )
	    user = cur.fetchone()
            self.fin_succ(**user)
        else:
            state = {'tel_phone':'token_error'}
            self.fin_succ(**state)
