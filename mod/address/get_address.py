from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
from mod.base.exceptions import ArgsError, PermissionDeniedError,OtherError


class GetAddressHandler(BaseHandler):
    @coroutine
    def post(self):
        token = self.get_json_argument("token")
        curuser = yield self.db.execute(#ensure the user exists
        "SELECT * FROM customer WHERE token=%s",
            (
                token
            )
        )
        if curuser.rowcount == 0:
            state = {'address':'token_error'}
            self.fin_succ(**state)
        else:
            user = curuser.fetchone()
            tel_phone=user["tel_phone"]
            cur = yield self.db.execute(
                "SELECT * FROM User_used_address WHERE tel_phone=%s order by is_def desc",
                (
                    tel_phone
                )
            )
        
            user = cur.fetchall()
            state={"address":user}
            self.fin_succ(**state)

			
