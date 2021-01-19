from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.core.files import uploadedfile
from .models import File
from .serializers import BaseSerializer, URLSerializer, FileSerializer, Base64Serializer

from PIL import Image
from urllib import request as url_request
import os

class FileView(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def checkRequestKey(self,request):
        if(not request.data.__contains__('file')):
            return [False,'file']
        elif(not request.data.__contains__('type')):
            return [False,'type']
        elif(not request.data.__contains__('name')):
            return [False,'name']
        elif(not request.data.__contains__('user_id')):
            return [False,'user_id']
        else: 
            return [True,'none'] 
        
    def checkName(self,request):
        revisedRequestData = request.data
        if(request.data.__contains__('name')):  # the picture is store at other key instead of key 'file'
            if(request.data.__contains__(request.data['name'])): # the key of image is valid
                keyOfImage = revisedRequestData['name']
                revisedRequestData['file'] = revisedRequestData[keyOfImage]
            else: # change the 'name' to default value: 'file'
                revisedRequestData['name'] = 'file' 
        else: # change the 'name' to default value: 'file'
            revisedRequestData['name'] = 'file' 
        return revisedRequestData 

#################################################################################

    def create(self, request, *args, **kwargs):
        # print(request.data)
        
        # check whether Request keys match the requirements 
        resultRequestKey = self.checkRequestKey(request)
        if(resultRequestKey[0] == False):
            return Response({'data':"Missing key '%s'. Please send request as the API spec." %(resultRequestKey[1]) ,'success':False, 'status':status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if(request.data['type'] == 'url'): # please make sure the POST header format is correct
            # print("serializer = URLSerializer")
            serializer = URLSerializer(data=request.data)
        elif(request.data['type'] == 'image'):
            # print("serializer = FileSerializer")
            if(isinstance(request.data['file'],uploadedfile.InMemoryUploadedFile)):
                revisedRequestData = self.checkName(request)
                serializer = FileSerializer(data=revisedRequestData)
            else:
                return Response({'data':"Wrong value of 'file'. Please upload gif, png or jpg under 5MB " ,'success':False, 'status':status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif(request.data['type'] == 'base64'):
            # print("serializer = Base64Serializer")
            serializer = Base64Serializer(data=request.data)
        else:
            return Response({'data':"'type' not right. Please send request as the API spec.",'success':False, 'status':status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        
        if serializer.is_valid():
            # print(serializer)
            serializer.save()

            container_index = self.getContainerIndex()
            container_path = '/container/' + container_index
            response_data = serializer.data
            media_path = response_data['file']
            response_data['file'] = container_path + media_path
            # print(response_data['file'])

            return Response({'data':response_data, 'success':True, 'status':status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        else:
            return Response({'data':serializer.errors,'success':False, 'status':status.HTTP_500_INTERNAL_SERVER_ERROR}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
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