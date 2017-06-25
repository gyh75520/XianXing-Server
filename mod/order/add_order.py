from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
import time
import shortuuid
import random
from mod.base.exceptions import ArgsError, PermissionDeniedError,OtherError

class AddOrderHandler(BaseHandler):
    @coroutine
    def post(self):
        token = self.get_json_argument("token")
        del_time = self.get_json_argument("del_time")
        address = self.get_json_argument("address")
        rec_phone = self.get_json_argument("rec_phone")
        user_name = self.get_json_argument("user_name")
        sex = self.get_json_argument("sex")
        food_id = self.get_json_argument("food_id")
        amount = self.get_json_argument("amount")
        start_time = self.get_json_argument("start_time")
        all_price = self.get_json_argument("all_price")
        pay_way = self.get_json_argument("pay_way")
        get_way = self.get_json_argument("get_way")
        PS = self.get_json_argument("PS")
        map_id = self.get_json_argument("map_id")
        del_pri = self.get_json_argument("del_pri")
        
        end_flag = False
        cur = yield self.db.execute(#ensure the user exists
        "SELECT * FROM customer WHERE token=%s",
            (
            token
            )
        )
        if cur.rowcount != 0:
            curmarket = yield self.db.execute(
                        "SELECT * FROM market WHERE map_id=%s",
                            (
                            map_id
                            )
                        )
            if curmarket.rowcount != 0:
                food_id_list = food_id.split(",")
                amount_list = amount.split(",")
                for i in range(len(food_id_list)):
                    curfood=yield self.db.execute(
                    "select food_name,surplus from food where food_id=%s",
                        (
                        food_id_list[i]
                        )
                    )
                    food =curfood.fetchone()
                    food_name =food["food_name"]
                    surplus =food["surplus"]
                    if int(amount_list[i])>surplus :
                        state = {'order':"not_enough"}
                        state["name"]=food_name
                        self.fin_succ(**state)
                        end_flag = True
                        break
                if end_flag !=True:
                    market = curmarket.fetchone()
                    market_id = market["market_id"] 
                    user = cur.fetchone()
                    tel_phone = user["tel_phone"]
                    order_num=shortuuid.uuid()
                    yield self.db.execute(
                    "INSERT INTO user_order(tel_phone,del_time,address,rec_phone,user_name,sex,start_time,all_price,pay_way,get_way,PS,market_id,del_pri,ostatus,order_num) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (
                        tel_phone,
                        del_time,
	                address,
                        rec_phone,
                        user_name,
                        sex,
                        start_time,
                        all_price,
                        pay_way,
                        get_way,
                        PS,
                        market_id,
                        del_pri,
                        1,
                        order_num,
                        )
                    )

                    curorder = yield self.db.execute(
                    "SELECT order_id FROM user_order WHERE order_num=%s",
                        (
                        order_num,
                        )
                    )
                    order=curorder.fetchone()
                    order_id=order["order_id"]
                    
                    st=int(tel_phone)+8888888888
                    new_order_num=str(order_id)
                    new_order_num+=str(st)
                    new_order_num+=str(random.randrange(1000,10000))
                    new_order_num=new_order_num[0:16]
                    yield self.db.execute(
                    "UPDATE user_order SET order_num=%s WHERE order_id=%s",
                        (
                        new_order_num,
                        order_id, 
                        )
                    )
                    for i in range(len(food_id_list)):
                        yield self.db.execute(
                        "INSERT INTO food_amount(food_id,amount,order_id) values (%s,%s,%s)",
                            (
                            food_id_list[i],
                            amount_list[i],
                            order_id,
                            )
                        )
                        yield self.db.execute(
                        "UPDATE food SET sales=sales+%s,surplus=surplus-%s WHERE food_id=%s",
                            (
                            amount_list[i], 
                            amount_list[i], 
                            food_id_list[i],
                            )
                        )
                    state = {'order':new_order_num}
                    self.fin_succ(**state)
            else:
                state = {'order':'map_id_error'}
                self.fin_succ(**state)
        else:
            state = {'order':'token_error'}
            self.fin_succ(**state)
        
            
