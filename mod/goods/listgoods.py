from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
from datetime import datetime
from mod.base.exceptions import ArgsError, PermissionDeniedError,OtherError

class ListGoodsHandler(BaseHandler):
    @coroutine
    def post(self):
	food_kind_1st = self.get_json_argument("food_kind_1st")
        cur = yield self.db.execute(
            "select name, type, price, spec, sales ,food_id ,url ,surplus from((select fk.food_kind_2st as name, 0 as type, fk.food_kind_id as fkid, null as price, null as spec ,null as sales,null as food_id,null as url,null as surplus from food_kind fk where fk.food_kind_1st = %s)union all(select f.food_name as name, 1 as type,f.food_kind_id as fkid, f.unit_price as price, f.spec as spec, f.sales as sales, f.food_id as food_id,f.url as url ,f.surplus as surplus from food f, food_kind fk where fk.food_kind_1st = %s and f.food_kind_id =fk.food_kind_id)order by fkid, type)as a;",
            (
            food_kind_1st,
	    food_kind_1st,
            )
        )
	if cur.rowcount == 0:
            result={"result":"food_kind_1st_error"}
	else:
	    ret=cur.fetchall();
            result={"result":ret}
        self.fin_succ(**result)
