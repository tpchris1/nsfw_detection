"""NSFW_detect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

import os

container_index = ''
try:
    f = open(os.path.join(os.getcwd(), 'container_index.txt' ), "r")
    container_index = f.read()
    f.close()
except:
    container_index= 'invalid "container_index". please check your bash/docker-compose/docker file'
container_index = container_index[0] # get rid of the newline character etc.
# print("container_index: " + container_index)

# api_url = 'api/' + settings.API_VERSION # remove version from url
api_url = 'api/'

urlpatterns = [
    path('container/' + container_index + '/admin/', admin.site.urls),
    path(api_url, include('detection_api.urls')),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
