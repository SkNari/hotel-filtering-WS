import requests
data ={
'start_date':'28_01_2021',
'nights':3,
'rooms':4,
'hotel_identifier':'2'
}

hotel = {
    'name':'Swing',
    'rooms':12
}

headers = {
    'token' : 'blablabla'
}

# r = requests.put('http://localhost:8082/bookings', data)
# r = requests.put('http://localhost:8082/hotels', hotel)
# r = requests.delete('http://localhost:8082/booking/2', headers = headers)

token = (requests.post('http://localhost:8080/api/login/', data = {'login': 'lucas', 'mdp': 'augusto'})).json()['token']
# r = requests.post('http://localhost:8080/api/checkToken', data = {'token': token})

# r = requests.delete('http://localhost:8082/booking/1', headers = {'token': token})
# r = requests.put('http://localhost:8082/hotels', headers = {'token': token}, data = hotel)
r = requests.put('http://localhost:8082/bookings', headers = {'token': 'token'}, data = data)
print(r.json())