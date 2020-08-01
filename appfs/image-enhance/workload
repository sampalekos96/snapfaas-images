from PIL import ImageEnhance, Image
import os
import base64
from io import BytesIO

def handle(request):
    imgpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), request['img'])
    img = Image.open(imgpath)
    op = request['op']
    if op == 'color':
        enhancer = ImageEnhance.Color(img)
    elif op == 'contrast':
        enhancer = ImageEnhance.Contrast(img)
    elif op == 'brightness':
        enhancer = ImageEnhance.Brightness(img)
    elif op == 'sharpness':
        enhancer = ImageEnhance.Sharpness(img)
    else:
        return {'success': 0, 'error': 'unknown enhancement mode'}
    factor = request['factor']
    enhanced_img = enhancer.enhance(factor)
    # serialized the enhanced image
    buff = BytesIO()
    enhanced_img.save(buff, format='JPEG')
    img_str = base64.b64encode(buff.getvalue()).decode()
    return {'success': 1, 'img_str': img_str}
