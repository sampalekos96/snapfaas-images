import json

def handle(obj, syscall): 
    route = '/repos/{}/{}/commits'.format(obj['owner'], obj['repo'])
    ret = syscall.github_rest_get(route)
    ret = json.loads(ret.data)
    commit_sha = ret[0]['sha']
    comment = 'This is a test comment'
    body = {}
    body['body'] = comment
    route = route + '/{}/comments'.format(commit_sha)
    ret = syscall.github_rest_post(route, body)
    return {'response': ret.data}
    
