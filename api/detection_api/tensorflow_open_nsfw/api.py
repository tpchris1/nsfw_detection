from . import my_classify_nsfw

def getPossibility(filepath): 
    '''use the file path to get the image and call original 'recognize()' function in my_classify_nsfw'''
    return my_classify_nsfw.recognize(filepath)


def getPossibilityStream(file):
    '''use the pillow image and call modified 'recognize_stream()' function in my_classify_nsfw'''
    return my_classify_nsfw.recognize_stream(file)