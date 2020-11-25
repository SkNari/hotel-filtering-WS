import requests

def check_token(token):
    r = requests.post('http://localhost:8083/api/checkToken', data = {'token': token}).json()
    if 'data' in r:
        return True, r['username']
    else:
        return False, False