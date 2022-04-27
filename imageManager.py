import PySimpleGUI as sg

from PIL import Image
import requests
from io import BytesIO


class ImageManager:

    def __init__(self) -> None:
        pass

    # Code to convert a URL to image data was taken form this help tread: https://github.com/PySimpleGUI/PySimpleGUI/issues/2941
    def image_to_data(im):

        with BytesIO() as output:
            im.save(output, format="PNG")
            data = output.getvalue()
        return data

    # Creates an image element from url
    def create_image(url, resize, key = None):

        response = requests.get(url, stream=True)
        response.raw.decode_content = True

        img = Image.open(response.raw)
        data = ImageManager.image_to_data(img)

        if(key != None):
            img_box = sg.Image(data=data, key = key, enable_events=True)
        else:
            img_box = sg.Image(data=data, enable_events=True)

        return img_box
