import hashlib
import time
import shortuuid
from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
from mod.base.exceptions import ArgsError, PermissionDeniedError,OtherError

class ChangePwdHandler(BaseHandler):

    @coroutine
    def post(self):
	#password = self.get_json_argument("password")
        tel_phone = self.get_json_argument("tel_phone")
	newpwd = self.get_json_argument("newpwd")
        #hashpassword = hashlib.md5(password.encode("utf-8")).hexdigest()

	cur = yield self.db.execute(
            "SELECT password FROM customer WHERE tel_phone=%s",
            (
                tel_phone
            )
        )
	if cur.rowcount != 0:
            token = hashlib.md5(shortuuid.uuid()+str(time.time())).hexdigest()
            newpwd = hashlib.md5(newpwd.encode("utf-8")).hexdigest()
	    user = cur.fetchone()
	    yield self.db.execute(
                "UPDATE customer SET password=%s ,token=%s WHERE tel_phone=%s",
                (
		    newpwd,
                    token,    
                    tel_phone,
                )
            )
            state = {'state':'success'}
            self.fin_succ(**state)
            
	else:
    	    state = {'state':'tel_phone_error'}
            self.fin_succ(**state)

