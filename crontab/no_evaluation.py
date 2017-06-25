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
    yield cur.execute("select start_time,order_id from user_order where ostatus=3")
    orders=cur.fetchall()
    for order in orders:
        days=(datetime.now()-order[0]).days
        if days>7:
            #print order[0]
            yield cur.execute("update user_order set ostatus=5 where order_id=%s",
                (
                order[1]
                )
            )
    conn.commit()
    cur.close()  
    conn.close()
    
ioloop.IOLoop.current().run_sync(main)
