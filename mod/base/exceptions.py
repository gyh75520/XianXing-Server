#coding=utf8
from tornado.web import  HTTPError
from mod.base import errors

class MissingArgumentError(HTTPError):
    def __init__(self, arg_name):
        super(MissingArgumentError, self).__init__(
            400, 'Missing argument %s' % arg_name)
        self.arg_name = arg_name
        self.code = errors.MISSING_ARGS

class PermissionDeniedError(HTTPError):
    def __init__(self,res_name):
        super(PermissionDeniedError,self).__init__(201,"用户权限不允许:{0}".format(res_name))
        self.arg_name = res_name
        self.code = errors.PERMISSIONS_DENIED

class ArgsError(HTTPError):
    def __init__(self,res_name):
        super(ArgsError,self).__init__(201,"参数错误:{0}".format(res_name))
        self.arg_name = res_name
        self.code = errors.ARGS_ERROR

class RelateResError(HTTPError):
    def __init__(self,res_name):
        super(RelateResError,self).__init__(201,"相关资源不存在:{0}".format(res_name))
        self.arg_name = res_name
        self.code = errors.RELATE_RES_ERROR

class OtherError(HTTPError):
    def __init__(self,res_name):
        super(OtherError,self).__init__(201,"其他错误:{0}".format(res_name))
        self.arg_name = res_name
        self.code = errors.OTHER_ERROR

class AuthorityError(HTTPError):
    def __init__(self,res_name):
        super(AuthorityError,self).__init__(201,"身份错误:{0}".format(res_name))
        self.arg_name = res_name
        self.code = errors.AUTHORITY_ERROR