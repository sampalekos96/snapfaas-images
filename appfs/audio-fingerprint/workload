from acoustid import fingerprint_file
import os

def handle(request):
    audiofilepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), request['audio'])
    duration, fp = fingerprint_file(audiofilepath)
    return {'duration': duration, 'fingerprint': fp.decode('utf-8')}
