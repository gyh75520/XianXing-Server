#coding=utf-8
import hashlib
import shortuuid
import time
from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
from mod.base.exceptions import ArgsError, PermissionDeniedError,OtherError


class UserHandler(BaseHandler):
    @coroutine
    def get(self):
        cur = yield self.db.execute(
            "select name, type, price, spec from ((select fk.food_kind_2st as name, 0 as type, fk.food_kind_id as fkid, null as price, null as spec from food_kind fk where fk.food_kind_1st = %s)union all(select f.food_name as name, 1 as type,f.food_kind_id as fkid, p.unit_price as price, p.spec as spec from food f, price p, food_kind fk where p.food_id = f.food_id and  fk.food_kind_1st = %s and f.food_kind_id = fk.food_kind_id and  p.market_id = 1)order by fkid, type)a",
            (
              "蔬菜",
	      "蔬菜",
            )
        )
	ret=cur.fetchall();
        result={"result":ret}
        
        #self.finish(json_encode(result))
 	self.fin_succ(**result)
        #self.fin_succ_array(result)
    @coroutine
    def put(self):
	password = self.get_json_argument("password")
        token = self.get_json_argument("token")
	newpwd = self.get_json_argument("newpwd")
        #hashpassword = hashlib.md5(password.encode("utf-8")).hexdigest()

	cur = yield self.db.execute(
            "SELECT password FROM customer WHERE token=%s",
            (
                token
            )
        )
	if cur.rowcount != 0:
            new_token = hashlib.md5(shortuuid.uuid()+str(time.time())).hexdigest()
            password = hashlib.md5(password.encode("utf-8")).hexdigest()
            newpwd = hashlib.md5(newpwd.encode("utf-8")).hexdigest()

	    user = cur.fetchone()
            if(password==user["password"]):
		yield self.db.execute(
                   "UPDATE customer SET password=%s ,token=%s WHERE token=%s",
                   (
		      newpwd,
                      new_token,    
                      token,
                   )
                )
                state = {'state':'success'}
                self.fin_succ(**state)
            else:
		state = {'state':'pwd_error'}
                self.fin_succ(**state)
	else:
    	    state = {'state':'token_error'}
            self.fin_succ(**state)
		
    @coroutine
    def post(self):
        password = self.get_json_argument("password")
        tel_phone = self.get_json_argument("tel_phone")
        nick_name = self.get_json_argument("nick_name")
        cur = yield self.db.execute(
            "SELECT * FROM customer WHERE tel_phone=%s",
            (
                tel_phone
            )
        )
        if cur.rowcount != 0:
            state = {'state':'already'}
            self.fin_succ(**state)
        else:
            token = hashlib.md5(shortuuid.uuid()+str(time.time())).hexdigest()
            password = hashlib.md5(password.encode("utf-8")).hexdigest()
            yield self.db.execute(
                "INSERT INTO customer(tel_phone,password,nick_name,token) VALUES(%s,%s,%s,%s)",
                (
                   tel_phone,
                   password,
                   nick_name,
                   token,
                )
            )
            state = {'state':'ok'}
            self.fin_succ(**state)
        
        

        

		

		
