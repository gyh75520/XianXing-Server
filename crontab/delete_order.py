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
    yield cur.execute("select start_time,order_id from user_order where ostatus=1")
    orders=cur.fetchall()
    for order in orders:
        seconds=(datetime.now()-order[0]).seconds
        if seconds>1800:
            #print order[0]
            yield cur.execute("select food_id,amount from food_amount where order_id=%s",
                (
                 order[1]
                )
            )
            foods = cur.fetchall()
            for food in foods:
                food_id = food[0]
                amount = food[1]
                yield cur.execute("UPDATE food SET surplus=surplus+%s WHERE food_id=%s",
                    (
                    amount, 
                    food_id,
                    )
                )
            yield cur.execute("DELETE FROM food_amount WHERE order_id=%s",
                (
                order[1],
                )
            )
            yield cur.execute("delete from user_order where order_id=%s",
                (
                order[1]
                )
            )
    conn.commit()
    cur.close()  
    conn.close()
    
ioloop.IOLoop.current().run_sync(main)
