import pymysql
import re
import traceback

import sys

host = "localhost"
# user="root"
# password="136614567977"
user = "gg"
password = "123456"
database = "yunlong"


# 得到所有已经插入的日期  只返回一个包含了所有日期的列表
def get_alldate():
    try:
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()
        date_list = []
        sql = "SELECT * FROM Room_list"
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            temp = re.findall(r'(.*)', str(row[0]))
            date_list.append(temp[0])
        return date_list
    except Exception as e:
        return "wrong"
    finally:
        cursor.close()
        conn.close()


# 得到所有订单编号
def get_allorderid():
    try:
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()
        date_list = []
        sql = "SELECT * FROM Room_order"
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            date_list.append(row[0])
        return date_list
    except Exception as e:
        return "wrong"
    finally:
        cursor.close()
        conn.close()


# 插入一个订单
def insertOneOrder(date, room):
    id = getid(room, date)
    try:
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()
        sql = "INSERT INTO Room_order(id) VALUES (%s) ;"
        cursor.execute(sql, [id])
        conn.commit()
    except:
        return "wrong"
    finally:
        cursor.close()
        conn.close()


# 更新订单信息
def update_order(date, room, name, contact, price, note):
    id = getid(room, date)
    print(date)
    try:
        # 连接database
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        sql = "UPDATE Room_order SET DATE='%s',Room='%s',Name='%s',Contact='%s',Price='%s',Note='%s' where id='%s';" % (
        date, room, name, contact, price, note, id)
        print(sql)
        cursor.execute(sql)
        conn.commit()
        return "right"
    except Exception as e:
        # 输出异常信息
        info = sys.exc_info()
        print(info[0], ":", info[1])
        conn.rollback()
        return "wrong"
    finally:
        cursor.close()
        conn.close()


# 删除订单
def delete_order(id):
    try:
        # 连接database
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        id = "'" + id + "'"
        sql = "delete from Room_order where id=%s" % (id);
        print(sql)
        cursor.execute(sql)
        conn.commit()
        return "right"
    except Exception as  e:
        info = sys.exc_info()
        print(info[0], ":", info[1])
        conn.rollback()
        return "wrong"
    finally:
        cursor.close()
        conn.close()


# 更新房间信息
def update_room(date, room, type):
    try:
        # 连接database
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        sql = "UPDATE Room_list SET Room" + room + " = '" + type + "' WHERE DATE= '" + date + "'";
        print(sql)
        cursor.execute(sql)
        # 提交事务
        conn.commit()
        return "right"
    except Exception as e:
        conn.rollback()
        return "wrong"
    finally:
        cursor.close()
        conn.close()


# 插入房间总列表
def order_a_room(date, room):
    try:
        # 连接database
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()

        sql = "INSERT INTO Room_list(date, Room" + room + ") VALUES (%s,%s) ;"
        cursor.execute(sql, [date, "ordered"])
        conn.commit()

        return "right"
    except Exception as e:
        conn.rollback()
        return "wrong"
    finally:
        cursor.close()
        conn.close()


# 得到一天的房间信息,返回一个包含了一整天的情况
def getOneDayRoomList(date):
    try:
        # 连接database
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        sql = "SELECT * FROM Room_list where date=%s"
        cursor.execute(sql, [date])
        results = cursor.fetchall()
        return list(results[0])
    except Exception as e:
        conn.rollback()
        return "wrong"
    finally:
        cursor.close()
        conn.close()

# 判断一个房间是不是在大表中却没有在订单中
def judgeroom(date,room):
    try:
        # 连接database
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        sql = "SELECT Room{room} FROM Room_list where date=%s".format(room=room)
        cursor.execute(sql, [date])
        results =  list(cursor.fetchall()[0])
        if (str(results[0])=="ordered"):
            return True
        else:
            return False
    except Exception as  e:
        info = sys.exc_info()
        print(info[0], ":", info[1])
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()




# 得到一个订单的完整信息
def getOneOrder(id):
    orderDetail = {}
    try:
        # 连接database
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        sql = "SELECT * FROM Room_order where id=%s"
        cursor.execute(sql, [id])
        print(sql)
        results = cursor.fetchall()
        orderDetail["name"] = results[0][3]
        orderDetail["contact"] = results[0][4]
        orderDetail["price"] = results[0][5]
        orderDetail["note"] = results[0][6]
        return orderDetail

    except Exception as e:
        conn.rollback()
        return "wrong"

    finally:
        cursor.close()
        conn.close()


def getid(room, date):
    temp = date.replace("-", "")
    id = temp + room
    return id


#
# list=["123","1999-5-30","101","大优老师","17317706748","100","testtesttesttestest"]
# for i in range(len(list)):
#     list[i]="'"+list[i]+"'"
# print(list)
# print(update_order(list[0],list[1],list[2],list[3],list[4],list[5],list[6]))

# print(delete_order("123"))
print(judgeroom("2019-11-21","101"))
