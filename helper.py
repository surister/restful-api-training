import requests
# import datetime

# r = requests.post('http://127.0.0.1:5000/user', json={'name': 'admin', 'password': 'admin'})
# r = requests.get('http://127.0.0.1:5000/login', auth=('admin', 'admin'))
# r = requests.post('http://127.0.0.1:5000/user/56bf9966-95ad-403d-bda1-873955354471', json={'key': 123})
# r = requests.delete('http://127.0.0.1:5000/user/56bf9966-95ad-403d-bda1-873955354471')
payload = {'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiIxZmJhNjgxOC1iNGFkLTQ1NjYtYTI1Yy1kMDhiODIzZmZkZmQiLCJleHAiOjE1MzYwNzc5Njl9.S3vEBYQZDJAK4QFOMiQ3PWpQLotNLz1pVeQIHLLgR9E'}
r = requests.get('http://127.0.0.1:5000/user', headers=payload)
# r = requests.get('x', auth=('usuario', 'contraseña'))
print(r, r.text)

