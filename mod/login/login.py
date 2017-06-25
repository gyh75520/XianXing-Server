import hashlib
from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
from datetime import datetime
import time
from mod.base.exceptions import ArgsError, PermissionDeniedError,OtherError


class LoginHandler(BaseHandler):
    @coroutine
    def post(self):
        password = self.get_json_argument("password")
        tel_phone = self.get_json_argument("tel_phone")
        password = hashlib.md5(password.encode("utf-8")).hexdigest()
        cur = yield self.db.execute(
            "SELECT password FROM customer WHERE tel_phone=%s",
            (
                tel_phone
            )
        )
        if cur.rowcount != 0:
            user = cur.fetchone()
            if(password==user["password"]):
                yield self.db.execute(
                "UPDATE customer SET last_log=%s WHERE tel_phone=%s",
                    (
                    time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()),
                    tel_phone,
                    )
                )
                cur = yield self.db.execute(
                    "SELECT tel_phone,nick_name,token FROM customer WHERE tel_phone=%s",
                    (
                    tel_phone
                    )
                )
                user = cur.fetchone()
                self.fin_succ(**user)
            
            else:
                state = {'tel_phone':'error'}
                self.fin_succ(**state)
        else:
            state = {'tel_phone':'error'}
            self.fin_succ(**state)
        
        

        

		

		
