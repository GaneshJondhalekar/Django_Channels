from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import time
import threading

class LoopData(threading.Thread):

    def __init__(self,total):
        threading.Thread.__init__(self)
        self.total=total

    try:
        def run(self):
            channel_layer=get_channel_layer()
            for i in range(1,self.total+1):
                
                
                percentage=int((i/self.total)*100)
                data={'count':i,'percentage':percentage}
                #here type is send_loop_data whci is method inside consumer we have called here and send value to it
                async_to_sync(channel_layer.group_send)(
                    "broadcast_group",{
                    'type':'send_loop_data',
                        'value':json.dumps(data)
                    }
                )
                
                time.sleep(0.5)
    except Exception as e:
        print(e)