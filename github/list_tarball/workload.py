import tarfile, io
def handle(obj, syscall):
    in_bytes = bytes(obj['tarball'])
    file_like = io.BytesIO(in_bytes)
    tar = tarfile.open(mode='r:gz', fileobj=file_like)
    return {'members': [x.name for x in tar.getmembers()]}
