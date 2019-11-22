var base_url = "http://127.0.0.1:5000/"
//var base_url="http://www.dayoulaoshi.cn/"


//input改动的实时更新
function addSelectTimeRefresh() {
    let date;
    let item = document.getElementById("select_date")
    item.onchange = function () {
        date = item.value;
        refresh(date)
    }
}

//打开的时候刷新
function openRefresh() {
    let d = new Date();
    let year = d.getFullYear();
    let month = d.getMonth() + 1;
    let day = d.getDate();
    date = year + "-" + month + "-" + day;
    date = formatDate(date)
    let item = document.getElementById("select_date");
    item.value = date;
    refresh(date);
}

//给每一个房间添加 "插入""删除""详情" 按钮
function addInsertDeleteButton() {
    let items = document.getElementsByTagName("p");
    for (let i = 0; i < items.length; i++) {
        if (items[i].getAttribute("class") === "room") {
            let whichRoom = items[i].getAttribute("title");
            //添加按钮
            buttonInsert = document.createElement("button")
            insertText = document.createTextNode("添加")
            buttonInsert.append(insertText);
            buttonInsert.onclick = function () {
                let date = document.getElementById("now_date").lastChild.nodeValue
                return insertRoom(whichRoom, date)
            }

            items[i].append(buttonInsert);
            //删除按钮
            buttonDelete = document.createElement("button")
            deleteText = document.createTextNode("删除")
            buttonDelete.append(deleteText);
            buttonDelete.onclick = function () {
                let date = document.getElementById("now_date").lastChild.nodeValue
                return deleteRoom(whichRoom, date)
            }
            items[i].append(buttonDelete);

            //详情按钮
            buttonDetail = document.createElement("button")
            detailText = document.createTextNode("详情")
            buttonDetail.append(detailText);
            buttonDetail.onclick = function () {

                let date = document.getElementById("now_date").lastChild.nodeValue
                showOneRoomDetail(whichRoom, date)

            }

            items[i].append(buttonDetail);
        }

    }
}

function formatDate(date) {                    //格式化日期
    date_list = date.split("-")

    if (date_list[1].length < 2)
        date_list[1] = "0" + date_list[1]
    if (date_list[2].length < 2)
        date_list[2] = "0" + date_list[2]

    return String(date_list[0] + "-" + date_list[1] + "-" + date_list[2])

}

window.onload = function () {
    addSelectTimeRefresh();
    addInsertDeleteButton();
    openRefresh();

}