def handle(obj, syscall): 
    route = '/repos/{}/{}'.format(obj['owner'], obj['repo'])
    ret = syscall.github_rest_get(route)
    return {'response': ret.data}
    
