function getNewContent (){
	var request=getHttpObject();
	if (request){
		request.open("GET","http://127.0.0.1:5000",true);
		request.onreadystatechange=function(){
			if (request.readyState==4){
				alert("a")
			}
		};
		request.send(null);
	}
	else{
		alert("sorry,wrong")
	}
	alert("b")
}

getNewContent()