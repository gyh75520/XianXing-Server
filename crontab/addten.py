from tornado import ioloop, gen
import tornado_mysql
from tornado.escape import json_encode,json_decode

@gen.coroutine
def main():
    conn =yield tornado_mysql.connect(host="127.0.0.1", user="root", passwd="root", db="bangzai", port=3306)
    cur = conn.cursor()
    yield cur.execute("update food set sales=sales+10")
    conn.commit()
    cur.close()
    conn.close()
ioloop.IOLoop.current().run_sync(main)





