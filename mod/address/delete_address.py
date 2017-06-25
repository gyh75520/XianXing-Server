from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
from mod.base.exceptions import ArgsError, PermissionDeniedError,OtherError


class DeleteAddressHandler(BaseHandler):
    @coroutine
    def post(self):
        token = self.get_json_argument("token")
        address_id=self.get_json_argument("address_id")
        curuser = yield self.db.execute(#ensure the user exists
        "SELECT * FROM customer WHERE token=%s",
            (
                token
            )
        )
        if curuser.rowcount == 0:
            state = {'state':'token_error'}
            self.fin_succ(**state)
        else:
            cur = yield self.db.execute(#ensure the address will be deleted exists
                "SELECT * FROM User_used_address WHERE address_id=%s",
                (
                    address_id
                )
            )
            if cur.rowcount != 0:
                address=cur.fetchone()
                user = curuser.fetchone()
                tel_phone=user["tel_phone"]
                yield self.db.execute(
                    "DELETE FROM User_used_address WHERE address_id=%s",
                    (
                    address_id
                    )
                )
                curAll=yield self.db.execute(#query the user has how many addresses
                "SELECT * FROM User_used_address WHERE tel_phone=%s",
                (
                    tel_phone
                )
                )
                if address["is_def"]==1 and curAll.rowcount>0:#if the deleted one is default and there still has addresses then set the id is smallest one be the default
                    addresses=curAll.fetchall()#get all addresses the user used.
                    ids=[]#to save the ids of the user's addresses.
                    for item in addresses:
                        ids.append(item["address_id"])
                    minId=min(ids)
                    yield self.db.execute("UPDATE User_used_address SET is_def=1 WHERE tel_phone=%s AND address_id=%s",(tel_phone,minId))
                state={"state":"success"}
                self.fin_succ(**state)
            else:
                state={"state":"id_error"}
                self.fin_succ(**state)
			
