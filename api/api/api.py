# TODO: 實現三個自動切換
# from . import cloudinary_api
# from . import sightengine_api
from .tensorflow_open_nsfw import classify_nsfw


def recognize(image_path):
    """
    return
    {
        possibility: float
    }
    """
    return classify_nsfw.recognize(image_path)
