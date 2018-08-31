import requests
import datetime

#r = requests.post('http://127.0.0.1:5000/user', json={'name': 'Surister', 'password': 'surister123'})
r = requests.get('http://127.0.0.1:5000/login', auth=('Surister', 'surister123'))
print(r, r.text)

