# django and djangorestframework
from django.core.files import File
from django.db import models
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.conf import settings
from django.db.models.signals import pre_delete # handle delete sync with admin db delete
from django.dispatch.dispatcher import receiver # handle delete sync with admin db delete
from django.utils.html import format_html

# some usual packages
import os
from urllib import request
from PIL import Image
import random
import string

# Create your models here.
class File(models.Model):
    file = models.ImageField(blank=False, null=False)
    type = models.CharField(max_length=20,blank=True)
    name = models.CharField(max_length=50,default='file')
    user_id = models.CharField(max_length=100,blank=True)

    possibility = models.FloatField(null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if(self.possibility > settings.DETECT_THRESHOLD): # DETECT_THRESHOLD = 0.6
            super().save(*args, **kwargs)
        # else:
            # print("possibitily:",str(self.possibility),"no save")

        if(self.type == 'url'):
            # print("Currently in save() of 'url' type ")
            media_path = settings.MEDIA_URL + self.file.name # unified with the 'image' method
            self.file = media_path;
        elif(self.type == 'image'):
            # print("Currently in save() of 'image' type ")
            pass
        elif(self.type == 'base64'):
            # print("Currently in save() of 'base64' type ")
            media_path = settings.MEDIA_URL + self.file.name # unified with the 'image' method
            self.file = media_path;
        return
    
    def fileLink(self):
        # print("Currently in fileLink()")
        container_index = self.getContainerIndex()
        container_path = '/container/' + container_index
        media_path = container_path + settings.MEDIA_URL + self.file.name
        link = format_html('<a href="{}">{}</a>',
                media_path,
                self.file.name,
            )
        if self.file:
            return link
        else:
            return format_html('<a>{}</a>','File Not Found')  
    fileLink.allow_tags = True
    fileLink.short_description = "Actual File Link"

    def getContainerIndex(self):
        container_index = ''
        try:
            f = open(os.path.join(os.getcwd(), 'container_index.txt' ), "r")
            container_index = f.read()
            f.close()
        except:
            container_index= 'invalid "container_index". please check your bash/docker-compose/docker file'
        container_index = container_index[0] # get rid of the newline character etc.
        # print("container_index: " + container_index)
        
        return container_index

@receiver(pre_delete, sender=File)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False) 