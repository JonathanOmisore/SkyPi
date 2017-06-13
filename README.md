# SkyPi
WebSockets are a relatively new technology that faciliates communication between the server and the web browser. SkyPi uses WebSockets to allow you to access your Raspberry Pi from any device with a web browser. Data is exchanged in JSON format. So far, it's only possible for the client to retrieve data from the Raspberry Pi. I am working on file transfer and other stuff.
## Dependencies:
### Client:
* Web browser that supports web sockets

### Raspberry Pi:
* Python >= 3.5
* Python with Asyncio package
* Python with WebSocket package

## Usage:
### On Raspberry Pi:
* python skypi.py [host] [port] [server password]
