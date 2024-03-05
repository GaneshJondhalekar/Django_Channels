from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

"""By default the send(), group_send(), group_add() and other functions are async functions, meaning you have to await them. 
If you need to call them from synchronous code, you ll need to use the handy asgiref.sync.async_to_sync wrapper:
"""
class MySocketConsumer(WebsocketConsumer):
    

    def connect(self):

        self.room_name="test_broudcast"
        self.room_group_name="test_broudcast_group"
        
        #add channel layer
        async_to_sync(self.channel_layer.group_add)(
           self.room_group_name, self.channel_name
        )
        # Called on connection.
        # To accept the connection call:
        self.accept()

        #send method used to send data from backend to frontend
        self.send(text_data=json.dumps({"STATUS":"WebSocket comsumer connect"}))
        
    #recieve method will receive data from frontend to backend 
    #javascript method 
    def receive(self, text_data=None, bytes_data=None):
        print(text_data)

    def disconnect(self, close_code):
        pass

    def send_notification(self,data):
        print(data)
        notification_data=json.loads(data.get('value'))
        self.send(text_data=json.dumps(notification_data)) #javascript method socket.onmessage will receive this data from backend


#disadvantages of websocketconsumer is it will not wait for data it will  give all data at a time.
#so we will use async websocket consumer as below

class MyConsumer(AsyncWebsocketConsumer):
    #groups = ["broadcast"]

    async def connect(self):

        self.room_name="broadcast"
        self.room_group_name="broadcast_group"

        await self.channel_layer.group_add(
            self.room_group_name,self.channel_name
        )
        # Called on connection.
        # To accept the connection call:
        await self.accept()

        await self.send(text_data=json.dumps({'status':"Connected to Async Websocket consumer"}))
        

    async def receive(self, text_data=None, bytes_data=None):
        print(text_data)

    async def disconnect(self, close_code):
        pass

    async def send_loop_data(self,data):
        print(data)
        loop_data=json.loads(data.get('value'))
        await self.send(text_data=json.dumps(loop_data))


