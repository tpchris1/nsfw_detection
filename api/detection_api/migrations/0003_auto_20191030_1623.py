# Generated by Django 2.2.6 on 2019-10-30 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detection_api', '0002_auto_20191021_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.CharField(default='file', max_length=50),
        ),
    ]
