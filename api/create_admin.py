import django
import os
from django.contrib.auth import get_user_model

def create_admin_func():
    User = get_user_model()
    User.objects.create_superuser('batalk', 'batalk@batalk.fun', 'batalk')
    return

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NSFW_detect.settings')
django.setup()
create_admin_func()