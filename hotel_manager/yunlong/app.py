import json
import re
import dealdatebase as dd

from flask import Flask, request
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("Home.html")


@app.route('/text')
def Home_page():
    return "The test data"


@app.route('/date', methods=['GET', 'POST'])
def date():
    if request.method == 'POST':
        get_date = request.get_data().decode('utf-8')
        return get_date

#点击预定时触发，作用是在两张表中都插入信息
@app.route('/insert_room', methods=['GET', 'POST'])
def insert_room():
    if request.method == 'POST':
        get_date = request.get_data().decode('utf-8')
        json_date = json.loads(get_date)
        print(json_date)
        room = json_date["Room"]
        date = json_date["date"]
        type = "ordered"
        insert_result = ""
        update_result = ""
        date_list = dd.get_alldate()

        order_result = dd.insertOneOrder(date, room)                                #插入一个订单

        if date not in date_list:
            insert_result = dd.order_a_room(date, room)                             #大表数据库中插入一个
        else:
            update_result = dd.update_room(date, room, type)

        if (insert_result == "right" or update_result == "right" or order_result == "right"):
            return "right"
        else:
            return "wrong"



#点击删除房间的时候触发，将大表中信息删除，同时删除订单
@app.route('/delete_room', methods=['GET', 'POST'])
def delete_room():
    if request.method == 'POST':
        get_date = request.get_data().decode('utf-8')
        json_date = json.loads(get_date)
        print(json_date)

        room = json_date["Room"]
        date = json_date["date"]
        type = "disordered"

        id = date.replace("-", "") + room
        order_result = dd.delete_order(id)                               #删除订单
        print("删除订单结果：" + order_result)
        date_list = dd.get_alldate()

        if date not in date_list:
            delete_result = "wrong"
        else:
            delete_result = dd.update_room(date, room, type)            #更新大表房间信息

        return delete_result


@app.route('/getOneDayRoomList', methods=['GET', 'POST'])
def getOneDayRoom():
    if request.method == 'POST':
        get_date = request.get_data().decode('utf-8')
        json_date = json.loads(get_date)
        print(json_date)
        date = json_date["date"]
        if date in dd.get_alldate():
            result = dd.getOneDayRoomList(date)
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

#这个按钮是用户点击详情之后触发的,查询数据库，返回一个订单的详细数据的json
@app.route('/getOneorder', methods=['GET', 'POST'])
def getOneorder():
    orderDetail = {}
    if request.method == 'POST':
        get_date = request.get_data().decode('utf-8')
        json_date = json.loads(get_date)
        id = json_date["date"].replace("-", "") + json_date["room"]
        orderIdList = dd.get_allorderid()

        if id in orderIdList:
            order=dd.getOneOrder(id)



            #None空字符串
            for key,value in order.items():
                if value is None:
                    order[key]=""

            orderDetail["type"] = "ordered"
            orderDetail["name"] = order["name"]
            orderDetail["contact"] = order["contact"]
            orderDetail["note"] = order["note"]
            orderDetail["price"] = order["price"]
        elif dd.judgeroom(json_date["date"],json_date["room"]) :
            dd.insertOneOrder(json_date["date"],json_date["room"])
            orderDetail["type"] = "ordered"
            orderDetail["name"] = ""
            orderDetail["contact"] = ""
            orderDetail["note"] =""
            orderDetail["price"] = ""
        else:
            orderDetail["type"] = "disordered"
        return orderDetail


#更新一个订单信息
@app.route('/changeOneOrder', methods=['GET', 'POST'])
def changeOneOrder():
    if request.method == 'POST':
        get_date = request.get_data().decode('utf-8')
        json_date = json.loads(get_date)


        type=dd.update_order(json_date["date"],json_date["room"],json_date["name"],json_date["contact"],json_date["price"],json_date["note"])
        result={"type":type}
        return result

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)  # 运行开始
