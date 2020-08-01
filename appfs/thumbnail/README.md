Generates thumbnail of the input image

The function now assumes the input images are copied to appfs and in the same diretory as function source code.

Function request should be like:
{'img': image name, 'size': target thumbnail size}

Function response is like:
{'serialized_img': serialized thumbnail}
