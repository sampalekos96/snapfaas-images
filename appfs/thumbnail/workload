from PIL import Image
import os
import base64
from io import BytesIO

def handle(request):
    imgpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), request['img'])
    img = Image.open(imgpath)
    img.thumbnail(request['size'])
    buff = BytesIO()
    img.save(buff, format='JPEG')
    img_str = base64.b64encode(buff.getvalue()).decode()
    return {'serialized_img': img_str}
