This function makes use of the open source [tesseract OCR engine](https://github.com/tesseract-ocr/tesseract).

This function currently assumes that all images are copied to appfs. That is all images
are locally avaliable to the guest VM.

Function request should be like:

{'img': image name}

Function response is like:

{'success': 0, 'error': error msg}

or

{'success': 1, 'text': tesseract output}
