#coding=utf-8
import os
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado_mysql import pools
from tornado_mysql.cursors import DictCursor
from tornado.options import options,define
from router.router import handlers

define("port",default=8000,help="本地监听端口",type=int)
define("db_host",default="127.0.0.1",help="数据库地址",type=str)
define("db_port",default=3306,help="数据库端口",type=int)
define("db_name",default="bangzai",help="数据库名",type=str)
define("db_user",default="root",help="数据库用户名",type=str)
define("db_password",default="root",help="数据库端口",type=str)

'''class MainHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db

    @coroutine
    def get(self):
        cur = yield self.db.execute('SELECT id FROM try',)
        a = cur.fetchone()
        self.finish(a)'''
'''没加cursorclass=DictCursor
   fetchone返回(187, "2", 1)
   加cursorclass=DictCursor 返回dict
   fetchone返回{"password": "2", "tel_phone": 187, "custom_id": 1}'''
class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
        )
        self.db = pools.Pool(
            dict(host=options.db_host, port=options.db_port, user=options.db_user,
                 passwd=options.db_password, db=options.db_name,cursorclass=DictCursor,charset='utf8'
                 ),
            max_idle_connections=1,
            max_recycle_sec=3,
            max_open_connections=2,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
