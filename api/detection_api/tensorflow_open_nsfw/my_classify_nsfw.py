#!/usr/bin/env python
import sys

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import argparse
import tensorflow as tf

from .model import OpenNsfwModel, InputType
from .image_utils import create_tensorflow_image_loader
from .image_utils import create_yahoo_image_loader
from .image_utils import create_yahoo_image_loader_stream

import numpy as np


IMAGE_LOADER_TENSORFLOW = "tensorflow"
IMAGE_LOADER_YAHOO = "yahoo"


def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("input_file", help="Path to the input image.\
                        Only jpeg images are supported.")

    parser.add_argument("-m", "--model_weights", required=True,
                        help="Path to trained model weights file")

    parser.add_argument("-l", "--image_loader",
                        default=IMAGE_LOADER_YAHOO,
                        help="image loading mechanism",
                        choices=[IMAGE_LOADER_YAHOO, IMAGE_LOADER_TENSORFLOW])

    parser.add_argument("-i", "--input_type",
                        default=InputType.TENSOR.name.lower(),
                        help="input type",
                        choices=[InputType.TENSOR.name.lower(),
                                 InputType.BASE64_JPEG.name.lower()])

    args = parser.parse_args()

    model = OpenNsfwModel()

    with tf.Session() as sess:

        input_type = InputType[args.input_type.upper()]
        model.build(weights_path=args.model_weights, input_type=input_type)

        fn_load_image = None

        if input_type == InputType.TENSOR:
            if args.image_loader == IMAGE_LOADER_TENSORFLOW:
                fn_load_image = create_tensorflow_image_loader(tf.Session(graph=tf.Graph()))
            else:
                fn_load_image = create_yahoo_image_loader()
        elif input_type == InputType.BASE64_JPEG:
            import base64
            fn_load_image = lambda filename: np.array([base64.urlsafe_b64encode(open(filename, "rb").read())])

        sess.run(tf.global_variables_initializer())

        image = fn_load_image(args.input_file)

        predictions = \
            sess.run(model.predictions,
                     feed_dict={model.input: image})

        print("Results for '{}'".format(args.input_file))
        print("\tSFW score:\t{}\n\tNSFW score:\t{}".format(*predictions[0]))

if __name__ == "__main__":
    main(sys.argv)

def recognize(image_path) -> dict:
    MODEL_WEIGHTS = os.path.dirname(os.path.abspath(
        __file__)) + os.sep + 'data/open_nsfw-weights.npy'
    IMAGE_LOADER = IMAGE_LOADER_YAHOO
    # choices=[InputType.TENSOR.name.lower(),InputType.BASE64_JPEG.name.lower()])
    model = OpenNsfwModel()
    tf.reset_default_graph()

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


# Added by tpchris1
def recognize_stream(stream_image) -> dict:
    MODEL_WEIGHTS = os.path.dirname(os.path.abspath(
        __file__)) + os.sep + 'data/open_nsfw-weights.npy'
    IMAGE_LOADER = IMAGE_LOADER_YAHOO
    # choices=[InputType.TENSOR.name.lower(),InputType.BASE64_JPEG.name.lower()])
    model = OpenNsfwModel()
    tf.reset_default_graph()

    with tf.Session() as sess:

        input_type = InputType.TENSOR
        model.build(weights_path=MODEL_WEIGHTS, input_type=input_type)

        fn_load_image = None

        if input_type == InputType.TENSOR:
            if IMAGE_LOADER == IMAGE_LOADER_TENSORFLOW:
                fn_load_image = create_tensorflow_image_loader(sess)
            else:
                fn_load_image = create_yahoo_image_loader_stream()
        elif input_type == InputType.BASE64_JPEG:
            pass
            # import base64
            # fn_load_image = lambda filename: np.array([base64.urlsafe_b64encode(open(filename, "rb").read())])

        sess.run(tf.global_variables_initializer())

        image = fn_load_image(stream_image)

        predictions = \
            sess.run(model.predictions,
                     feed_dict={model.input: image})
        """
        predictions[0] # list of SFW, NSFW
        """
        return {'possibility': predictions[0][1]}