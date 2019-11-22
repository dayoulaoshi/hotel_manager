layui.use('layer', function () {
    var layer = layui.layer;
});

//插入房间基本操作
function insertRoom(room, date) {
    date = formatDate(date)
    var truthBeTold = window.confirm("日期：" + date + "\n房间号：" + room + "\n确认预定？")
    if (truthBeTold) {
        post = getHttpObject();
        url = base_url + "insert_room"
        post.open('Post', url, true);
        post.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        post.send(JSON.stringify({
            "date": date,
            "Room": room
        }));
        post.onreadystatechange = function () {
            if (post.readyState == 4 && post.status == 200) {
                text = post.responseText
                if (text == 'right') {
                    var string = "预定成功！\n" + "日期：" + date + "\n房间号：" + room;
                    refresh(date)
                    alert(string)
                } else if (text == "wrong") {
                    alert("预定失败")
                }
            }
        }
    } else {
    }
    return false;
}

//删除房间基本操作
function deleteRoom(room, date) {
    date = formatDate(date)
    var truthBeTold = window.confirm("日期：" + date + "\n房间号：" + room + "\n确认取消预定？")
    if (truthBeTold) {
        post = getHttpObject();
        url = base_url + "delete_room"
        post.open('Post', url, true);
        post.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        post.send(JSON.stringify({
            "date": date,
            "Room": room
        }));
        post.onreadystatechange = function () {
            if (post.readyState == 4 && post.status == 200) {
                text = post.responseText
                if (text == 'right') {
                    var string = "取消预定成功\n" + "日期：" + date + "\n房间号：" + room;
                    refresh(date)
                    alert(string)
                } else if (text == "wrong") {
                    alert("取消预定失败")
                }
            }
        }
    } else {

    }
    return false;
}

//刷新基本操作
function refresh(date) {
    date = formatDate(date)
    post = getHttpObject();
    url = base_url + "getOneDayRoomList"
    post.open('Post', url, true);
    post.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    post.send(JSON.stringify({
        "date": date
    }));
    post.onreadystatechange = function () {
        if (post.readyState == 4 && post.status == 200) {
            text = post.responseText;
            let json_text = JSON.parse(text);
            let now_date = document.getElementById("now_date")
            now_date.lastChild.nodeValue = json_text["date"]
            let image_ordered = "static/images/ordered.png"
            let image_disordered = "static/images/no_ordered.png"
            for (let item in json_text) {
                if (item == "date") {
                    continue;
                }
                let room = document.getElementById(item)
                let status = json_text[item]
                if (status == "ordered") {
                    room.src = image_ordered
                }
                if (status == "disordered") {
                    room.src = image_disordered
                }
            }
        }
    }
}

//更新一个订单信息
function changeRoomOrder(date,room,name,contact,price,note){
    date = formatDate(date);
    post = getHttpObject();
    url = base_url + "changeOneOrder";
    post.open('Post', url, true);
    post.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    post.send(JSON.stringify({
        "date": date,
        "room":room,
        "name":name,
        "contact":contact,
        "price":price,
        "note":note
    }));
     post.onreadystatechange = function () {
         if (post.readyState == 4 && post.status == 200) {
             text = post.responseText;
             let json_text = JSON.parse(text);
             type=json_text["type"]
         }
         else {
             type="wrong"
         }
     }
     return type;
}





//点击详情后触发
function showOneRoomDetail(room, date) {
    post = getHttpObject();
    url = base_url + "getOneorder"
    post.open('Post', url, true);
    post.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    post.send(JSON.stringify({
        "date": date,
        "room": room
    }));
    post.onreadystatechange = function () {
        if (post.readyState == 4 && post.status == 200) {

            text = post.responseText;
            let json_text = JSON.parse(text);
            if (json_text["type"] == "disordered") {
                alert("还没有预定")
            } else if (json_text["type"] == "ordered") {
                orderDetail=layer.open({
                    title: "详情"
                    , content: "姓名：" + json_text["name"] + "<br>"
                        + "联系方式：" + json_text["contact"] + "<br>"
                        + "成交价格：" + json_text["price"] + "<br>"
                        + "备注：" + json_text["note"] + "<br>"
                    , btn: ['编辑', '退出']
                    , yes: function () {
                        layer.close(orderDetail)
                        changeOrder=layer.open({
                            type: 1 //Page层类型
                            , area: ['500px', '300px']
                            ,
                            btn: ["确定", "取消"]
                            ,
                            title: '修改订单'
                            ,
                            skin: 'layui-layer-prompt'
                            ,
                            content: "<div class=''>" +
                                "<div>姓名&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;：<input title=\"name\" type='text'  value='"+json_text["name"] +"'></div>" +
                                "<div>联系方式：<input title=\"contact\" type='text'  value='"+json_text["contact"] +"'></div>" +
                                "<div>成交价格：<input title=\"price\"type='text'  value='"+json_text["price"] +"'></div>" +
                                "<div>备注&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;：<input title=\"note\" type='text'  value='"+json_text["note"] +"'></div>" +
                                "</div>"
                            ,
                            yes: function (index, layero) {
                                //按钮【按钮一】的回调

                                Name=$(layero).find("input[title='name']").val();
                                contact=$(layero).find("input[title='contact']").val();
                                price=$(layero).find("input[title='price']").val();
                                note=$(layero).find("input[title='note']").val();

                                type=changeRoomOrder(date,room,Name,contact,price,note)

                                if(type=="wrong")
                                    alert("失败")
                                else if (type=="right")
                                    alert("更新成功")
                                layer.close(changeOrder)
                            }
                        });
                    }

                });

            }
        }
    }

}
