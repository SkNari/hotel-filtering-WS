import requests
data ={
'name':'Erwan',
'surname':'Vallerie',
'start_date':'30_11_2020',
'nights':8,
'rooms':9,
'hotel_identifier':'1'
}

hotel = {
    'name':'Aurion',
    'rooms':12
}


# r = requests.put('http://localhost:8082/bookings', data)
# r = requests.put('http://localhost:8082/hotels', hotel)
r = requests.delete('http://localhost:8082/booking/2')