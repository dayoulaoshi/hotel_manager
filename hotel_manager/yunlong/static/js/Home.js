var base_url="http://127.0.0.1:5000/"
//var base_url="http://www.dayoulaoshi.cn/"


//input改动的实时更新
function addSelectTimeRefresh(){
	let date;
	let item=document.getElementById("select_date")
	item.onchange=function () {
		date=item.value;
		refresh(date)
	}
}

//打开的时候刷新
function openRefresh(){
	let d=new Date();
	let year=d.getFullYear();
	let month=d.getMonth()+1;
	let day=d.getDate();
	let date=year+"-"+month+"-"+day;
	let item=document.getElementById("select_date");
	item.value=date;
	refresh(date)
}

//给每一个房间添加插入删除按钮
function addInsertDeleteButton(){
	let items=document.getElementsByTagName("p");
	for(let i=0; i<items.length;i++){
		if(items[i].getAttribute("class")==="room"){
			let whichRoom=items[i].getAttribute("title");
			//添加按钮
			buttonInsert=document.createElement("button")
			insertText=document.createTextNode("添加")
			buttonInsert.append(insertText);
			buttonInsert.onclick=function(){
				let date=document.getElementById("now_date").lastChild.nodeValue
				return insertRoom(whichRoom,date)
			}

			items[i].append(buttonInsert);
			//删除按钮
			buttonDelete=document.createElement("button")
			deleteText=document.createTextNode("删除")
			buttonDelete.append(deleteText);
			buttonDelete.onclick=function(){
				let date=document.getElementById("now_date").lastChild.nodeValue
				return deleteRoom(whichRoom,date)
			}

			items[i].append(buttonDelete);
		}

	}
}

//插入房间基本操作
function insertRoom(room,date){
	var truthBeTold = window.confirm("日期："+date+"\n房间号："+room+"\n确认预定？")
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
					var string = "预定成功！\n" + "日期："+date + "\n房间号：" + room;
					refresh(date)
					alert(string)
				} else if (text == "wrong") {
					alert("预定失败")
				}
			}
		}
	}else {

	}
	return false;
}

//删除房间基本操作
function deleteRoom(room,date){
	var truthBeTold = window.confirm("日期："+date+"\n房间号："+room+"\n确认取消预定？")
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
					var string = "取消预定成功\n" + "日期："+date+"\n房间号："+room;
					refresh(date)
					alert(string)
				} else if (text == "wrong") {
					alert("取消预定失败")
				}
			}
		}
	}else{

	}
	return false;
}
//刷新基本操作
function refresh(date){
	post=getHttpObject();
	url=base_url+"getOneDayRoomList"
	post.open('Post', url, true);
	post.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	post.send(JSON.stringify({
		"date":date
	}));
	post.onreadystatechange=function(){
		if (post.readyState==4 && post.status==200){
			text = post.responseText;
			let json_text = JSON.parse(text);
			let now_date=document.getElementById("now_date")
			now_date.lastChild.nodeValue=json_text["date"]
			let image_ordered="static/images/ordered.png"
			let image_disordered="static/images/no_ordered.png"
			let test=document.getElementById("Room101")
			test.src=image_ordered
			for (let item in json_text){
				if (item=="date"){
					continue;
				}
				let room=document.getElementById(item)
				let status=json_text[item]
				if(status=="ordered"){
					room.src=image_ordered
				}
				if(status=="disordered"){
					room.src=image_disordered
				}
			}
		}
	}
}

window.onload=function(){
	addSelectTimeRefresh();
	addInsertDeleteButton();
	openRefresh();

}