#coding=utf8
from tornado.escape import json_encode,json_decode
from tornado.web import RequestHandler
from datetime import datetime
from mod.base.exceptions import MissingArgumentError,PermissionDeniedError
from mod.base import errors

class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db

    #body.decode("utf-8")表示将utf-8编码的字符串转换成unicode编码
    @property
    def json_body(self):
        if not hasattr(self,'_json_body'):
            if hasattr(self.request,"body"):
                self._json_body = json_decode(self.request.body.decode("utf-8"))
                return self._json_body
            else:
                return None
        else:
            return self._json_body

    def get_json_argument(self,name):
        if name in self.json_body:
            return self.json_body[name]
        else:
            raise MissingArgumentError(name)

    def fin_succ(self,*args,**kwargs):
        #self.set_header("Content-type","appliction/json")
        if len(args) != 0:
            self.finish(json_encode(args))
        elif len(args) == 0 and len(kwargs) != 0:
            self.finish(json_encode(kwargs))
        else:
            kwargs['state'] = 'ok'
            self.finish(kwargs)

    def fin_succ_array(self,array):
        #self.set_header("Content-type","appliction/json")
        #判定array是list，否则将自动跑出AssertionError
        assert isinstance(array,list)
        self.finish(json_encode(array))

    def fin_error(self,reason,code):
        reason = str(reason)
        code = int(code)
        #self.set_header("Content-type","appliction/json")

        self.finish(json_encode(
            dict(
                reason = reason,
                code = code,
                state = 'error')
        ))

    def write_error(self,status_code,**kwargs):
        if(isinstance(kwargs["exc_info"][1],AssertionError)):
            self.set_status(401)
            self.fin_error("某参数格式不正确",errors.ARGS_ERROR)
            return

        if hasattr(kwargs["exc_info"][1],"code"):
            self.set_status(status_code)
            self.fin_error(str(kwargs["exc_info"][1]),code=kwargs["exc_info"][1].code)
        else:
            self.set_status(status_code)
            self.fin_error(str(kwargs["exc_info"][1]),code=999)
