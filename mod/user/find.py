import hashlib
from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
from datetime import datetime
from mod.base.exceptions import ArgsError, PermissionDeniedError,OtherError


class FindHandler(BaseHandler):
    @coroutine
    def post(self):
        tel_phone = self.get_json_argument("tel_phone")
        cur = yield self.db.execute(
            "SELECT tel_phone,nick_name,token FROM customer WHERE tel_phone=%s",
            (
                tel_phone
            )
        )
        if cur.rowcount != 0:
	    user = cur.fetchone()
            self.fin_succ(**user)
        else:
            state = {'tel_phone':'error'}
            self.fin_succ(**state)
