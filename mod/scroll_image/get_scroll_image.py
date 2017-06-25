from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler

class GetScrollImageHandler(BaseHandler):
    @coroutine
    def get(self):
        cur = yield self.db.execute("select url from scroll_image")
        scroll_image = cur.fetchall();
        state = {'scroll_image':scroll_image}
        self.fin_succ(**state)
