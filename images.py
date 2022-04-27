from PIL import Image
import requests
import PySimpleGUI as sg
from io import BytesIO

def image_to_data(im):
    """
    Image object to bytes object.
    : Parameters
      im - Image object
    : Return
      bytes object.
    """
    with BytesIO() as output:
        im.save(output, format="PNG")
        data = output.getvalue()
    return data

url = "https://picsum.photos/200/300"
response = requests.get(url, stream=True)
response.raw.decode_content = True
img = Image.open(response.raw)
data = image_to_data(img)
img_box = sg.Image(data=data)

window = sg.Window('', [[img_box]])
while True:
    event, values = window.read()
    if event is None:
        break
window.close()