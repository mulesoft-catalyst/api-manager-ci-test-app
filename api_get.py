import requests


resp = requests.get('https://reqres.in/api/users')
if resp.status_code != 200:
    raise ApiError('API call error'.format(resp.status_code))


print(resp.json()['data'])

