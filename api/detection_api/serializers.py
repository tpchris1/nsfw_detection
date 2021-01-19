# django and djangorestframework
from rest_framework import serializers
from django.conf import settings
from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework import status

# this app of django project
from .models import File

# some usual packages
import os
from io import BytesIO
from PIL import Image
from urllib import request
import random
import string
import base64

# nsfw_detection
from .tensorflow_open_nsfw import api


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


            
class URLSerializer(serializers.ModelSerializer):
    class Meta(BaseSerializer.Meta):
        model = BaseSerializer.Meta.model
        fields = BaseSerializer.Meta.fields

    file = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        # print("Currently in create() of URLSerializer")
        file = validated_data.pop('file')
        type = validated_data.pop('type')
        name = validated_data.pop('name')
        user_id = validated_data.pop('user_id')
        
        retrieved_image = self.getRemoteImage(file)
        possibility = getPossibilityStream(retrieved_image)
        if(possibility > 0.6):
            filename = self.saveImage(retrieved_image,True)
        else:
            filename = self.saveImage(retrieved_image,False)

        return File.objects.create(file=filename,type=type,name=name,user_id=user_id,possibility=possibility)
    
    def getRemoteImage(self,file):
        try:
            url = str(file)
            result = request.urlretrieve(url)
            # print(result)
        except:
            raise serializers.ValidationError({"data":"Can not retrieve the url of image. Please provide correct url.","success":False,"status":status.HTTP_500_INTERNAL_SERVER_ERROR})
        try:
            im = Image.open(result[0])
        except:
            raise serializers.ValidationError({"data":"Can not analyze the format of downloaded image. Please provide url with .jpg, .png or .gif image.","success":False,"status":status.HTTP_500_INTERNAL_SERVER_ERROR})
        
        if(im.format!='JPG' and im.format!='JPEG'):
            im = im.convert('RGB')
        # im.show()
        return im

    def saveImage(self,file,is_save):
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        filename = 'url_' + salt + ".jpg";
        filepath = settings.MEDIA_ROOT + '/' + filename;
        if(is_save):
            file.save(filepath,format='jpeg')
        return filename



class FileSerializer(serializers.ModelSerializer):
    class Meta(BaseSerializer.Meta):
        model = BaseSerializer.Meta.model
        fields = BaseSerializer.Meta.fields

    def create(self, validated_data):
        # print("Currently in create() of FileSerializer")
        # print(validated_data)
        file = validated_data.pop('file')
        type = validated_data.pop('type')
        name = validated_data.pop('name')
        user_id = validated_data.pop('user_id')


        retrieved_image = self.getPillowImage(file)
        self.checkImageFormat(retrieved_image)
        possibility = getPossibilityStream(retrieved_image)
        
        return File.objects.create(file=file,type=type,name=name,user_id=user_id,possibility=possibility)
    
    def getPillowImage(self, file):
        checkFile = BytesIO(file.file.read())
        im = Image.open(checkFile)
        if checkFile.getbuffer().nbytes > settings.MAX_IMAGE_UPLOAD_SIZE:
            raise serializers.ValidationError({"data":"Image size too big. Please upload gif, png or jpg under 5MB.","success":False,"status":status.HTTP_500_INTERNAL_SERVER_ERROR})
        return im

    def checkImageFormat(self, image):
        if image.format not in ('GIF', 'PNG', 'JPEG'):
            raise serializers.ValidationError({"data":"Unsupport image type. Please upload gif, png or jpg under 5MB.","success":False,"status":status.HTTP_500_INTERNAL_SERVER_ERROR})
        return



class Base64Serializer(serializers.ModelSerializer):
    class Meta(BaseSerializer.Meta):
        model = BaseSerializer.Meta.model
        fields = BaseSerializer.Meta.fields

    file = serializers.CharField()

    def create(self, validated_data):
        # print("Currently in create() of Base64Serializer")
        # print(validated_data)
        file = validated_data.pop('file')
        type = validated_data.pop('type')
        name = validated_data.pop('name')
        user_id = validated_data.pop('user_id')

        file,retrieved_image = self.convertToContentFile(file)
        possibility = getPossibilityStream(retrieved_image)

        return File.objects.create(file=file,type=type,name=name,user_id=user_id,possibility=possibility)

    
    def convertToContentFile(self, file):
        image_data = file
        try:
            format, imgstr = image_data.split(';base64,')
            # print("format", format)
            ext = format.split('/')[-1]
            salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            byte_image = base64.b64decode(imgstr)
            pil_image = Image.open(BytesIO(byte_image))  
            data = ContentFile(byte_image, name='base64_' + salt + '.' + ext) # You can save this as file instance.
        except:
            raise serializers.ValidationError({"data":"This is not a Base64 format image. Please upload correct format of Base64 image.","success":False,"status":status.HTTP_500_INTERNAL_SERVER_ERROR})
        return [data,pil_image]

def getPossibilityStream(image):
    result = api.getPossibilityStream(image)
    return result['possibility']