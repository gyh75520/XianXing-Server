from tornado import ioloop, gen
import tornado_mysql
from tornado.escape import json_encode,json_decode
import time

@gen.coroutine
def main():
    conn =yield tornado_mysql.connect(host="127.0.0.1", user="root", passwd="root", db="bangzai", port=3306)
    cur = conn.cursor()
    curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    yield cur.execute("update user_order set ostatus=4,remark_time=%s where ostatus=3",
        (
        curtime,
        )
    )
    yield cur.execute("update user_order set ostatus=3,rec_time=%s where ostatus=2",
        (
        curtime,
        )
    )
    yield cur.execute("update user_order set ostatus=2,jd_time=%s where ostatus=1",
        (
        curtime,
        )
    )
    conn.commit()
    cur.close()
    conn.close()
    
ioloop.IOLoop.current().run_sync(main)
