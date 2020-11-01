import os
import subprocess

SCRIPT_DIR=os.path.dirname(os.path.abspath(__file__))
TESS_DIR=os.path.join(SCRIPT_DIR, 'tesseract')
LIB_DIR=os.path.join(TESS_DIR, 'lib')
BINARY=os.path.join(TESS_DIR, 'bin', 'tesseract')
DATA_DIR=os.path.join(TESS_DIR, 'share', 'tessdata')

def handle(request):
    imgfilepath = os.path.join(SCRIPT_DIR, request['img'])
    command = 'LD_LIBRARY_PATH={} TESSDATA_PREFIX={} {} {} {}'.format(
        LIB_DIR,
        DATA_DIR,
        BINARY,
        imgfilepath,
        'stdout',
    )

    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        return {'succeed': 0, 'error': e.output}
    return {'succeed': 1, 'text': output.decode('utf-8')}
