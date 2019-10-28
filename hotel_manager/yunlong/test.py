# 导入pymysql模块
import re

import pymysql

#得到所有已经插入的日期
def get_alldate():
    try:
        conn = pymysql.connect(host="localhost", user="gg", password="123456", database="yunlong")
        cursor = conn.cursor()
        date_list=[]
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

# 插入房间（）
def insert_room(date,room):
    try:
        # 连接database
        conn = pymysql.connect(host="localhost", user="gg",password="123456",database="yunlong")
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        sql = "INSERT INTO Room_list(date, Room"+room+") VALUES (%s,%s) ;"
        cursor.execute(sql, [date,"ordered"])
        # 提交事务
        conn.commit()
        return "right"
    except Exception as e:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

#更新房间信息
def update_room(date,room,type):
    try:
        # 连接database
        conn = pymysql.connect(host="localhost", user="gg",password="123456",database="yunlong")
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        sql = "UPDATE Room_list SET Room"+room+" = '"+type+"' WHERE DATE= '"+date+"'";
        print(sql)
        cursor.execute(sql)
        # 提交事务
        conn.commit()
        return "right"
    except Exception as e:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

#得到一天的房间信息
def getOneDayRoomList(date):
    try:
        # 连接database
        conn = pymysql.connect(host="localhost", user="gg",password="123456",database="yunlong")
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        sql  = "SELECT * FROM Room_list where date=%s"
        cursor.execute(sql,[date])
        results = cursor.fetchall()
        return list(results[0])
    except Exception as e:
        conn.rollback()
        return "wrong"
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # type="ordered"
    # date="2000-07-12"
    # room="101"
    # date_list=get_alldate()
    # if date not in date_list:
    #     insert_room(date, room)
    # else:
    #     update_room(date,room,type)

    # room = "101"
    # date = "2000-05-12"
    # type = "disordered"
    #
    # delete_result = ""
    #
    # date_list = get_alldate()
    #
    # if date not in date_list:
    #     delete_result = "wrong"
    # else:
    #     delete_result = update_room(date, room, type)
    #
    # print(delete_result)


    date="2019-5-01"

    if date in get_alldate():
        result=getOneDayRoomList(date)
        for i in range(len(result)):
            if result[i] is None:
                result[i]="disorder"
        room_list={}
        room_list["date"] = re.findall(r'(.*)', str(result[0]))[0]
        room_list["Room101"]=result[1]
        room_list["Room102"]=result[2]
        room_list["Room103"]=result[3]
        room_list["Room105"]=result[4]
        room_list["Room106"]=result[5]
        room_list["Room107"]=result[6]
        room_list["Room108"]=result[7]
        room_list["Room109"]=result[8]
        room_list["Room201"]=result[9]
        room_list["Room202"]=result[10]
        room_list["Room203"]=result[11]
        room_list["Room301"]=result[12]
        room_list["Room302"]=result[13]

        print(room_list)
    else:
        room_list = {}
        room_list["date"] = date
        room_list["Room101"] = "disordered"
        room_list["Room102"] = "disordered"
        room_list["Room103"] = "disordered"
        room_list["Room105"] = "disordered"
        room_list["Room106"] = "disordered"
        room_list["Room107"] = "disordered"
        room_list["Room108"] = "disordered"
        room_list["Room109"] = "disordered"
        room_list["Room201"] = "disordered"
        room_list["Room202"] = "disordered"
        room_list["Room203"] = "disordered"
        room_list["Room301"] = "disordered"
        room_list["Room302"] = "disordered"
        print(room_list)

