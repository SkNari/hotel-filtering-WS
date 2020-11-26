# Web Service Python REST

Lucas AUGUSTO
Erwan VALLERIE
ENSIIE 2020

# Installation

You need to use pip to install every required packages

```python
pip install flask
pip install flaskrestfull
pip install markdown
```

# Run

```shell
python3 run.py
```

## Usage

All responses will have the form

json Success
```json Success
{
    "data": "Mixed type holding the content of the responce",
}
```

json Error
```json Error
{
    "message": "Description of what happened if there is an error"
}
```

## Definition

***Get***

Get every hotels
`Get /hotels`

Get a specific hotel
`Get /hotel/<string:identifier>`

Get every bookings
`Get /bookings`

Get a specific booking
`Get /booking/<string:identifier>`
`Get /booking/<string:username>`

Get every available hotel for a request
`Get /ask_booking?start_date=<XX DAY>_<XX MONTH>_<XXXX YEAR>&nights=<number_of_nights>&rooms=<number_of_rooms>`

***Put***

Add a hotel with an id, a name and a number of rooms
`Put /hotels       arguments : 'identifier', 'name', 'rooms'`

Add a booking with an id, a name, a surname, a start date, a number of nights and a hotel id
`Put /bookings     arguments : 'identifier', 'name', 'surname', 'start_date (XX_XX_XXXX)', 'nights', 'hotel_identifier'`

***Delete***

Delete a specific hotel
`Delete /hotel/<string:identifier>`

Delete a specific booking
`Delete /booking/<string:identifier>`

**Response**

- `200 OK` on success
- `400 ERROR` data not correct
- `403 ERROR` invalid authentification
- `404 ERROR` url not found


