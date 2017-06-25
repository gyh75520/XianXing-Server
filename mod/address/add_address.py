from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
from mod.base.exceptions import ArgsError, PermissionDeniedError,OtherError


class AddAddressHandler(BaseHandler):

    @coroutine
    def post(self):
        token = self.get_json_argument("token")
        user_name=self.get_json_argument("user_name")
        sex=self.get_json_argument("sex") 
        rec_phone=self.get_json_argument("rec_phone")
        address=self.get_json_argument("address")
        detail_addr=self.get_json_argument("detail_addr")
        is_def=self.get_json_argument("is_def")
        lng=self.get_json_argument("lng")
        lat=self.get_json_argument("lat")

        cur = yield self.db.execute(#ensure the user exists
        "SELECT * FROM customer WHERE token=%s",
            (
                token
            )
        )
        if cur.rowcount != 0:
            user = cur.fetchone()
            if is_def==1 or is_def=="1":#if the new address be seted default then update the old default not
                yield self.db.execute("UPDATE User_used_address SET is_def=0 WHERE tel_phone=%s AND is_def=1",(user["tel_phone"]))
            yield self.db.execute(#insert the new address
            "INSERT INTO User_used_address(tel_phone,user_name,sex,rec_phone,address,detail_addr,is_def,lng,lat) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                user["tel_phone"],
                user_name,
                sex,
	            rec_phone,
                address,
		          detail_addr,
	            is_def,
                lng,
                lat,
                )
            )
            state = {'state':'success'}
            self.fin_succ(**state)
        else:
            state = {'state':'token_error'}
            self.fin_succ(**state)
