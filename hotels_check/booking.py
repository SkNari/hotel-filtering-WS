import markdown
import os
import shelve
import datetime

from flask import Flask, g
from flask_restful import Resource, Api, reqparse

from hotels_check import hotel

def get_booking_db():
    db = getattr(g, "_database2", None)
    if db is None:
        db = g._database2 = shelve.open("booking.db")
    return db

class BookingList(Resource):
    def get(self):
        shelf = get_booking_db()
        keys = list(shelf.keys())

        bookings = []
    
        for key in keys:
            bookings.append(shelf[key])
            print(shelf[key])

        return {'data': bookings}, 200
    
    def put(self):
        parser = reqparse.RequestParser()

        # Déparasage de tous les arguments
        parser.add_argument('name', required = True)
        parser.add_argument('surname', required = True)
        parser.add_argument('start_date', required = True)
        parser.add_argument('nights', required = True)
        parser.add_argument('rooms', required = True)
        parser.add_argument('hotel_identifier', required = True)

        #Parse the arguments into an object
        args = parser.parse_args()
        
        # Récupération de la base de données des bookings
        shelf_booking = get_booking_db()

        # Incrémentation de l'id
        id_book = str(len(shelf_booking)+1)
        args['identifier'] = id_book

        shelf_booking[id_book] = args

        return {'data' : args}, 201
    
class Booking(Resource):
    def get(self, identifier):
        shelf = get_booking_db()

        if not identifier in shelf:
            return {'messages': 'Booking not found'}, 404
        
        return {'data': shelf[identifier]}, 200

    def delete(self, identifier):
        shelf = get_booking_db()

        if not identifier in shelf:
            return {'messages': 'Booking not found'}, 404

        del shelf[identifier]

        return {''}, 204