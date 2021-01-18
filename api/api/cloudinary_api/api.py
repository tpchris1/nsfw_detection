import configparser
import os

import cloudinary
import cloudinary.uploader

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))) + os.sep + 'config.ini')

cloudinary.config(
    cloud_name=config['cloudinary']['cloud_name'],
    api_key=config['cloudinary']['api_key'],
    api_secret=config['cloudinary']['api_secret']
)


def recognize(image_path):
    result = cloudinary.uploader.upload(image_path, moderation="aws_rek")
    return result
