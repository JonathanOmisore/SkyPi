var websocket;
var remotehostinfo;
var password;

function start(host,port){
		websocket = new WebSocket("ws://" + host + ":" + port); 
		websocket.onopen = function(event){
			password = $("#password").val();
	console.log("Open");
	var jsonsend = {"command": "requestaccess", "host": "localhost","password": password};
websocket.send(JSON.stringify(jsonsend));

	
	};
websocket.onmessage = function(event){
	remotehostinfo = JSON.parse(event.data);
	console.log(remotehostinfo);
	displayresponse(remotehostinfo);
	};
	websocket.onclose = function(event){
		alert("The connection has been closed.");
		
		
	};
	
	
}

function displayresponse(obj){
	switch(obj["response"]){
		case "requestaccess":
		if(obj["permission"] == "allowed"){
			$("#nameenter").hide();
	$("#commandenter").show();
	$("#status").text("You have been granted access");

			
		}
		else{
			$("#status").text(obj["response"]);
		}
		break;
	case "hostinfo":
		$("#system").text("Operating system: " + obj["system"] + " " + obj["release"]);
	$("#host").text("Host name: " + obj["host"]);
	break;
	case "listdirectories":
		$("#response").html("<pre>" + obj["directories"] + "</pre>");
		
	}
	


}

