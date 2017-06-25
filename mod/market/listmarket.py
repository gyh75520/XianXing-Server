from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
from datetime import datetime
from mod.base.exceptions import ArgsError, PermissionDeniedError,OtherError

class ListMarketsHandler(BaseHandler):
    @coroutine
    def post(self):
        map_ids=self.get_json_argument("map_id")
        map_id_list=map_ids.split(",")
        markets=[]
        for map_id in map_id_list:
            cur = yield self.db.execute(
                "SELECT address,market_name,score,sales,sta_pri,del_pri,free_pri,cha_phone FROM market WHERE map_id = %s",
                (
                 map_id     
                )
            )
            if cur.rowcount != 0:
	        market=cur.fetchone()
                markets.append(market)
        state = {'market':markets}
        self.fin_succ(**state)
        
        
            
