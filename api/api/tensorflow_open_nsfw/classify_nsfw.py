import os

import numpy as np
import tensorflow as tf

try:
    from model import OpenNsfwModel, InputType
    from image_utils import create_tensorflow_image_loader
    from image_utils import create_yahoo_image_loader
except ModuleNotFoundError:
    from .model import OpenNsfwModel, InputType
    from .image_utils import create_tensorflow_image_loader
    from .image_utils import create_yahoo_image_loader


IMAGE_LOADER_TENSORFLOW = "tensorflow"
IMAGE_LOADER_YAHOO = "yahoo"


def recognize(image_path) -> dict:
    MODEL_WEIGHTS = os.path.dirname(os.path.abspath(
        __file__)) + os.sep + 'data/open_nsfw-weights.npy'
    IMAGE_LOADER = IMAGE_LOADER_YAHOO
    # choices=[InputType.TENSOR.name.lower(),InputType.BASE64_JPEG.name.lower()])
    model = OpenNsfwModel()

    with tf.Session() as sess:

        input_type = InputType.TENSOR
        model.build(weights_path=MODEL_WEIGHTS, input_type=input_type)

        fn_load_image = None

        if input_type == InputType.TENSOR:
            if IMAGE_LOADER == IMAGE_LOADER_TENSORFLOW:
                fn_load_image = create_tensorflow_image_loader(sess)
            else:
                fn_load_image = create_yahoo_image_loader()
        elif input_type == InputType.BASE64_JPEG:
            pass
            # import base64
            # fn_load_image = lambda filename: np.array([base64.urlsafe_b64encode(open(filename, "rb").read())])

        sess.run(tf.global_variables_initializer())

        image = fn_load_image(image_path)

        predictions = \
            sess.run(model.predictions,
                     feed_dict={model.input: image})
        """
        predictions[0] # list of SFW, NSFW
        """
        return {'possibility': predictions[0][1]}
