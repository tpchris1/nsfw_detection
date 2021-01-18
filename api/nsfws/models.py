# Create your models here.
import os
from urllib import request

from django.core.files import File
from django.db import models
from PIL import Image

from api.api import recognize


class Nsfw(models.Model):

    possibility = models.FloatField(null=True)
    image = models.ImageField(upload_to='nsfw', null=True)
    image_url = models.URLField(null=True)

    class Meta:
        db_table = "nsfw"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        get_remote_image(self)
        get_nudity_possibility(self)


def get_remote_image(self):
    if self.image_url and not self.image:
        result = request.urlretrieve(self.image_url)
        self.image.save(
            os.path.basename(get_clear_image_name(self.image_url)),
            File(open(result[0], 'rb'))
        )
        self.save()


def get_clear_image_name(image_url):
    return image_url.split('?')[0]


def png_to_jpg(self):
    im = Image.open(self.image.path)
    rgb_im = im.convert('RGB')
    rgb_im.save('colors.jpg')
    # TODO: save to image
    self.save()


def get_nudity_possibility(self):
    if self.image and not self.possibility:
        result = recognize(self.image.path)
        self.possibility = result['possibility']
        self.save()
