from tornado.gen import coroutine
from mod.base.base import BaseHandler
from mod.base.exceptions import ArgsError, PermissionDeniedError,OtherError

class ChangenickHandler(BaseHandler):
    @coroutine
    def post(self):
        token = self.get_json_argument("token")
        nick_name = self.get_json_argument("nick_name")
        cur = yield self.db.execute(
            "SELECT * FROM customer WHERE token=%s",
            (
                token
            )
        )
        if cur.rowcount != 0:
	    user = cur.fetchone()
	    yield self.db.execute(
                "UPDATE customer SET nick_name=%s WHERE token=%s",
                (
	            nick_name,
                    token,
                )
            )
	    state = {'state':'success'}
            self.fin_succ(**state)
        else:
            state = {'state':'token_error'}
            self.fin_succ(**state)
