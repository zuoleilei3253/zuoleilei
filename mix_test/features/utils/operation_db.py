import pymysql
from features.steps.config import host,port,user,password,db,charset

# 封装函数用于select操作
def my_db1(sql):
    cn = pymysql.connect(host=host, user=user, password=password,
                         db=db,
                         port=port, autocommit=True)
    cursor = cn.cursor()
    cursor.execute(sql)
    cn.commit()
    rex = cursor.fetchall()
    cursor.close()
    cn.close()
    return rex


# 封装函数用于insert、delete、update
def my_db2(sql):
    co = pymysql.connect(host=host, user=user, password=password,
                         db=db,
                         port=port, autocommit=True)
    cur = co.cursor()
    try:
        cur.execute(sql)
        co.commit()
        res = cur.fetchall()
        return res
    except:
        co.rollback()
    cur.close()
    co.close()

