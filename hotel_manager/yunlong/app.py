import json
import re

import pymysql
from flask import Flask, request
from flask import Flask,render_template
app = Flask(__name__)

host="localhost"

#user="root"
#password="136614567977"

user="gg"
password="123456"


database="yunlong"


#得到所有已经插入的日期
def get_alldate():
    try:
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
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

# 插入房间
def order_a_room(date,room):
    try:
        # 连接database
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        sql = "INSERT INTO Room_list(date, Room"+room+") VALUES (%s,%s) ;"
        cursor.execute(sql, [date,"ordered"])
        # 提交事务
        conn.commit()
        return "right"
    except Exception as e:
        conn.rollback()
        return "wrong"
    finally:
        cursor.close()
        conn.close()

#更新房间信息
def update_room(date,room,type):
    try:
        # 连接database
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
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
        return "wrong"
    finally:
        cursor.close()
        conn.close()

#得到一天的房间信息
def getOneDayRoomList(date):
    try:
        # 连接database
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
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


@app.route('/')
def hello_world():
    return render_template("Home.html")

@app.route('/text')
def Home_page():
    return "The test data"

@app.route('/date',methods=['GET','POST'])
def date():
    if request.method=='POST':
        get_date=request.get_data().decode('utf-8')
        return get_date

@app.route('/insert_room',methods=['GET','POST'])
def insert_room():
    if request.method=='POST':
        get_date=request.get_data().decode('utf-8')
        json_date = json.loads(get_date)
        print(json_date)

        room=json_date["Room"]
        date=json_date["date"]
        type="ordered"

        insert_result=""
        update_result=""
        date_list = get_alldate()
        if date not in date_list:
            insert_result=order_a_room(date, room)
        else:
            update_result=update_room(date, room, type)

        if (insert_result=="right" or update_result=="right"):
            return "right"
        else:
            return "wrong"

@app.route('/delete_room',methods=['GET','POST'])
def delete_room():
    if request.method=='POST':
        get_date=request.get_data().decode('utf-8')
        json_date = json.loads(get_date)
        print(json_date)

        room=json_date["Room"]
        date=json_date["date"]
        type="disordered"

        delete_result=""

        date_list = get_alldate()

        if date not in date_list:
            delete_result="wrong"
        else:
            delete_result=update_room(date, room, type)

        return delete_result

@app.route('/getOneDayRoomList',methods=['GET','POST'])
def getOneDayRoom():
    if request.method=='POST':
        get_date=request.get_data().decode('utf-8')
        json_date = json.loads(get_date)
        print(json_date)
        date=json_date["date"]
        if date in get_alldate():
            result = getOneDayRoomList(date)
            for i in range(len(result)):
                if result[i] is None:
                    result[i] = "disorder"

            room_list = {}
            room_list["date"] = re.findall(r'(.*)', str(result[0]))[0]
            room_list["Room101"] = result[1]
            room_list["Room102"] = result[2]
            room_list["Room103"] = result[3]
            room_list["Room105"] = result[4]
            room_list["Room106"] = result[5]
            room_list["Room107"] = result[6]
            room_list["Room108"] = result[7]
            room_list["Room109"] = result[8]
            room_list["Room201"] = result[9]
            room_list["Room202"] = result[10]
            room_list["Room203"] = result[11]
            room_list["Room301"] = result[12]
            room_list["Room302"] = result[13]

            return room_list
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
            return room_list


if __name__ == '__main__':
       app.run(debug=True,host='0.0.0.0', port=80)  # 运行开始
