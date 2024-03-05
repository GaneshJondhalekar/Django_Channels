from django.shortcuts import render,HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import time

from .threading import LoopData
# Create your views here.
def index(request):

    return render(request,'index.html')


def task(request):
    total=request.GET.get('total')
    LoopData(int(total)).start() #here we have called thread
    return HttpResponse("Done")

def index1(request):

    channel_layer=get_channel_layer()
    for i in range(1,11):
        
        data={'count':i}
        #here type is send_notification which in method called which is avilable in consumer
        async_to_sync(channel_layer.group_send)(
            "test_broudcast_group",{
               'type':'send_notification',
                'value':json.dumps(data)
            }
        )
        time.sleep(1)
    return render(request,'index.html')