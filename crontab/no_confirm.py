from tornado import ioloop, gen
import tornado_mysql
from tornado.escape import json_encode,json_decode
from datetime import datetime

@gen.coroutine
def main():
    conn =yield tornado_mysql.connect(host="127.0.0.1", user="root", passwd="root", db="bangzai", port=3306)
    cur = conn.cursor()
    #curtime=time.strftime("%Y-%m-%d %X",time.localtime())
    #curtime=time.localtime()
    yield cur.execute("select start_time,order_id from user_order where ostatus=2")
    orders=cur.fetchall()
    for order in orders:
        days=(datetime.now()-order[0]).days
        print days
        if days>1:
            yield cur.execute("update user_order set ostatus=3,rec_time=%s where order_id=%s",
                (
                datetime.now(),
                order[1]
                )
            )
    conn.commit()
    cur.close()  
    conn.close()
    
ioloop.IOLoop.current().run_sync(main)
