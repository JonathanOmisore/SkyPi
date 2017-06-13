import asyncio
import websockets
import json
import sys
import os
import platform
import socket
print("server open")
address = sys.argv[1]
port = int(sys.argv[2])
password = sys.argv[3]
def ispasswordcorrect(jsondata):
    data = json.loads(jsondata)
    if data["password"] != password:
        return False
    elif "password" not in data:
        return False
    else:
        return True
def listdirectories():
    directories = os.listdir("/home/pi")
    temp = ""
    dirs = {"response":"listdirectories"}
    for x in directories:

        temp += x + "\n"
        dirs["directories"] = temp
    return  dirs
def hostinfo():
    info = {"response": "hostinfo", "system":platform.system(),"release":platform.release(), "host":socket.gethostname()}
    return info
def action(data):
    if data["command"] == "listdirectories":
        return listdirectories()    
    elif data["command"] == "hostinfo":
        return hostinfo()
    else:
        return {"response": "Nothing"}
def isjson(jsonthing):
    try:
        jsondata = json.loads(jsonthing)
    except:
        return False
    return True
    
async def start(websocket, path):
    
    while True:
        data = await websocket.recv()
        if not isjson(data):
            deniedmessage = {"response": "ACCESS DENIED"}
            await websocket.send(json.dumps(deniedmessage))
            websockets.close(start,address,port)
            
      
        elif not ispasswordcorrect(data):
            deniedmessage = {"response": "ACCESS DENIED"}
            await websocket.send(json.dumps(deniedmessage))
            websockets.close(start,address,port)
        else:
            jsondata = json.loads(data)
            connected = "{} connected".format(jsondata["host"])
            print(connected)
            print(jsondata["command"])
            if jsondata["command"] == "requestaccess":
                
                await websocket.send(json.dumps({"response":"requestaccess", "permission":"allowed"}))
            else:
                await websocket.send(json.dumps(action(jsondata))) 
start_server = websockets.serve(start,address, port)


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
