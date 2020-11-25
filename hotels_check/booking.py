from hotels_check.auth import check_token
import shelve
import datetime

from flask import Flask, g, request
from flask_restful import Resource, Api, reqparse

def get_booking_db():
    db = getattr(g, "_database2", None)
    if db is None:
        db = g._database2 = shelve.open("booking.db")
    return db

def delta_date(Date1, nights, Date2):
        nights_date = datetime.timedelta(days = int(nights))
        nul_date = datetime.timedelta(days = int(0))
        if(Date1 - Date2 > nul_date):
            if(Date1 - Date2 - nights_date >= nul_date):
                return 1
            else:
                return 0
        elif(Date1 - Date2 < nul_date):
            if(Date1 - Date2 + nights_date <= nul_date):
                return 1
            else:
                return 0
        else:
            return 0

class BookingList(Resource):
    def get(self):
        shelf = get_booking_db()
        keys = list(shelf.keys())

        parser = reqparse.RequestParser()

        parser.add_argument('surname', required = False)
        args = parser.parse_args()

        bookings = []

        if(args['surname']!=None):
            for key in keys:
                if shelf[key]['username'] == args['surname'] :
                    bookings.append(shelf[key])
        else:
            for key in keys:
                bookings.append(shelf[key])

        return {'data': bookings}, 200
    
    def put(self):
        token = request.headers.get('token')
        res_token = check_token(token)
        if res_token[0] == 1:

            parser = reqparse.RequestParser()

            # Déparasage de tous les arguments
            parser.add_argument('start_date', required = True)
            parser.add_argument('nights', required = True)
            parser.add_argument('rooms', required = True)
            parser.add_argument('hotel_identifier', required = True)

            #Parse the arguments into an object
            args = parser.parse_args()
            args['username'] = res_token[1]
            # Récupération de la base de données des bookings
            shelf_booking = get_booking_db()

            array_start_date = args['start_date'].split("_")

            nights = int(args['nights'])
            rooms = int(args['rooms'])
            # Vérification de la conformité des arguments
            if(nights <= 0):
                return {'message': 'Night can\'t be nul or negative'}, 400
            if(rooms <= 0 ):
                return {'message': 'Rooms can\'t be nul or negative'}, 400
            if(len(array_start_date) != 3):
                return {'message': 'Date not correct '}, 400 
            if(int(array_start_date[0]) < 0 or int(array_start_date[0]) > 31):
                return {'messages': f'Date (day : {array_start_date[0]}) not correct '}, 400
            if(int(array_start_date[1]) < 0 or int(array_start_date[1]) > 12):
                return {'messages': f'Date (month : {array_start_date[1]}) not correct '}, 400

            # Overwrite (annule toutes les réservations sur la même période)
            actual_date = datetime.date.today()

            start_date = datetime.date(int(array_start_date[2]), int(array_start_date[1]), int(array_start_date[0]))
            
            if(start_date < actual_date):
                return {'message': 'Date not correct '}, 400

            keys = list(shelf_booking.keys())

            for key in keys:
                array_booking_start_date = shelf_booking[key]['start_date'].split("_")
                booking_start_date = datetime.date(int(array_booking_start_date[2]), int(array_booking_start_date[1]), int(array_booking_start_date[0]))
                booking_nights = shelf_booking[key]['nights']
                if(not delta_date(start_date,nights,booking_start_date) and not delta_date(booking_start_date, booking_nights, start_date)):
                    Booking.delete(None,shelf_booking[key]['identifier'])
                
            # Incrémentation de l'id
            id_book = str(len(shelf_booking)+1)
            args['identifier'] = id_book

            shelf_booking[id_book] = args

            return {'data' : args}, 201

        else:
            return {'messages': 'Bad token'}, 403

class Booking(Resource):
    def get(self, identifier):
        shelf = get_booking_db()

        if not identifier in shelf:
            return {'messages': 'Booking not found'}, 404
        
        return {'data': shelf[identifier]}, 200

    def delete(self, identifier):
        token = request.headers.get('token')
        res_token = check_token(token)

        if res_token[0] == 1:

            shelf = get_booking_db()

            if not identifier in shelf:
                return {'messages': 'Booking not found'}, 404
            del shelf[identifier]

            return {''}, 204

        else:
            return {'messages': 'Bad token'}, 403