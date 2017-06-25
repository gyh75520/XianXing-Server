from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler
from mod.base.json_encoder import MyEncoder
import json

class ListEvaluationsHandler(BaseHandler):
    @coroutine
    def get(self):
        cur = yield self.db.execute("select remark,remark_time,remark_score,nick_name from(select  u.remark as remark,u.remark_time as remark_time,u.remark_score as remark_score, c.nick_name as nick_name from user_order u ,customer c where u.tel_phone=c.tel_phone and(u.remark_score is not null or u.remark is not null))as a;")
        evaluations = cur.fetchall()
        eva = {'evaluations':evaluations}
        state =json.dumps(eva, cls=MyEncoder)
        self.finish(state)
