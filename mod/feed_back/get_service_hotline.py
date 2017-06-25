from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler

class GetServiceHotlineHandler(BaseHandler):
    @coroutine
    def get(self):
        state = {'tel_phone':'400-888-8888'}
        self.fin_succ(**state)
