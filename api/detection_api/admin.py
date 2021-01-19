from django.contrib import admin

# Register your models here.
from .models import File

class apiAdmin(admin.ModelAdmin):
    fields = ['type', 'name', 'possibility','fileLink']
    list_display = ['id', 'image_filename']
    readonly_fields = ['fileLink']
    pass

    def image_filename(self,obj):
        return obj.file.name

admin.site.register(File, apiAdmin)