from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync

import json

from channels.layers import get_channel_layer
# Create your models here.

class Notification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    is_seen=models.BooleanField(default=False)
    text=models.CharField(max_length=100,blank=True)

    def save(self,*args,**kwargs):
        channel_layer=get_channel_layer()

        count=Notification.objects.filter(is_seen=False).count()
        current_notification=self.text

        data={'count':count,'current_notification':current_notification}
        #here we send data to consumer group "test_broudcast_group" having method send_notification
        async_to_sync(channel_layer.group_send)(
            "test_broudcast_group",{
                'type':'send_notification',
                'value':json.dumps(data)

            }
        )
        return super().save(*args,**kwargs)