from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler


class GetFoodKind1stHandler(BaseHandler):
    @coroutine
    def get(self):
        cur = yield self.db.execute("select distinct food_kind_1st from food_kind")
        food_kind_1st = cur.fetchall()
        food_list={"food_kind_1st_list":food_kind_1st}
        self.fin_succ(**food_list)
