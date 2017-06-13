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
def ispasswordcorrect(passw):
    if passw != password:
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
async def start(websocket, path):
    
    while True:
        data = await websocket.recv()
        jsondata = json.loads(data)
        print(data)
        print(jsondata)
        if not ispasswordcorrect(jsondata["password"]):
            deniedmessage = {"response": "ACCESS DENIED"}
            await websocket.send(json.dumps(deniedmessage))
            websockets.close(start,'192.168.1.122',8765)
        else:
            connected = "{} connected".format(jsondata["host"])
            print(connected)
            print(jsondata["command"])
            if jsondata["command"] == "requestaccess":
                
                await websocket.send(json.dumps({"response":"requestaccess", "permission":"allowed"}))
            else:
                await websocket.send(json.dumps(action(jsondata))) 
start_server = websockets.serve(start, '192.168.1.122', 8765)


asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
