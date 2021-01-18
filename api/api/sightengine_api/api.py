import configparser
import os

from sightengine.client import SightengineClient

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))) + os.sep + 'config.ini')


API_USER = config['sightengine']['api_user']
API_SECRET = config['sightengine']['api_secret']


def recognize(image_path):
    """
    {
        "status": "success",
        "request": {
            "id": "req_48vmgcgo5L7HTSQFsyK7V",
            "timestamp": 1542389326.9524,
            "operations": 3
        },
        "weapon": 0.0055,
        "alcohol": 0.001,
        "drugs": 0.001,
        "nudity": {
            "raw": 0.827,
            "safe": 0.077,
            "partial": 0.096
        },
        "offensive": {
            "prob": 0.01
        },
        "media": {
            "id": "med_48vm0wMQEgMsnvnUKn4i8",
            "uri": "photo.jpg"
        }
    }
    """

    client = SightengineClient(API_USER, API_SECRET)
    output = client.check(
        'nudity', 'wad', 'offensive').set_file(image_path)

    return output
