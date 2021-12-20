import tarfile, io
def handle(obj, syscall):
    route = '/repos/{}/tarball'.format(obj['repository']['full_name'])
    rsp = syscall.github_rest_get(route).data
    in_bytes = bytes(rsp)
    file_like = io.BytesIO(in_bytes)
    tar = tarfile.open(mode='r:gz', fileobj=file_like)
    return {'members': [x.name for x in tar.getmembers()]}
