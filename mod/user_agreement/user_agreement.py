from tornado.escape import json_encode,json_decode
from tornado.gen import coroutine
from mod.base.base import BaseHandler

class UserAgreementHandler(BaseHandler):
    @coroutine
    def get(self):
        self.render("user_agreement.html")
