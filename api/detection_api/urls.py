from django.urls import include,path
from rest_framework.routers import DefaultRouter

from .views import FileView

router = DefaultRouter()
router.register('nsfw', FileView, base_name='nsfw')

urlpatterns = [
    path('',include(router.urls)),
]