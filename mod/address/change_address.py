from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
from mod.base.exceptions import ArgsError, PermissionDeniedError,OtherError


class ChangeAddressHandler(BaseHandler):
    @coroutine
    def post(self):
        token = self.get_json_argument("token")
        address_id=self.get_json_argument("address_id")
        user_name=self.get_json_argument("user_name")
        sex=self.get_json_argument("sex")
        rec_phone=self.get_json_argument("rec_phone")
        address=self.get_json_argument("address")
        detail_addr=self.get_json_argument("detail_addr")
        is_def=self.get_json_argument("is_def")
        lng=self.get_json_argument("lng")
        lat=self.get_json_argument("lat")
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
            user = curuser.fetchone()
            tel_phone=user["tel_phone"]
            cur = yield self.db.execute(#check the address_id is or not exists.
                "SELECT * FROM User_used_address WHERE address_id=%s",
                (
                    address_id
                )
            )
            curAll= yield self.db.execute(
                "SELECT * FROM User_used_address WHERE tel_phone=%s",
                (
            	    tel_phone
                )
            )
            if cur.rowcount != 0:
                changeAddress=cur.fetchone()
                if is_def==1 or is_def=="1":#if the new address be seted default then update the old default not
                    yield self.db.execute("UPDATE User_used_address SET is_def=0 WHERE tel_phone=%s AND is_def=1",(tel_phone))
                if (changeAddress["is_def"]==1 or changeAddress["is_def"]=="1")and (is_def==0 or is_def=="0"):#if the address be seted not default then set the id which is littlest be the default
                    addresses=curAll.fetchall()#get all addresses the user used.
                    ids=[]#to save the ids of the user's addresses.
                    for item in addresses:
                        ids.append(item["address_id"])
                    ids.remove(address_id)#if the address_id is the min id then we should remove it or it will be set default
                    if len(ids)>0:
                        minId=min(ids)
                        yield self.db.execute("UPDATE User_used_address SET is_def=1 WHERE tel_phone=%s AND address_id=%s",(tel_phone,minId))
                yield self.db.execute(
                    "UPDATE User_used_address SET tel_phone=%s,user_name=%s,sex=%s,rec_phone=%s,address=%s,detail_addr=%s,is_def=%s,lng=%s,lat=%s WHERE address_id=%s",
                    (
                       tel_phone,
                       user_name,
                       sex,
                       rec_phone,
                       address,
		       detail_addr,
                       is_def,
                       lng,
                       lat,
                       address_id,
                    )
                )
                state={"state":"success"}
                self.fin_succ(**state)
            else:
                state = {'state':'id_error'}
                self.fin_succ(**state)
