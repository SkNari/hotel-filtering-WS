import markdown
import os
import shelve
import datetime

from flask import Flask, g
from flask_restful import Resource, Api, reqparse

from hotels_check import booking

def get_hotels_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = shelve.open("hotels.db")
    return db


class HotelsList(Resource):
    def delta_date(self, Date1, nights, Date2):
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

    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('start_date', required = False)
        parser.add_argument('nights', required = False)
        parser.add_argument('rooms', required = False)
        args = parser.parse_args()

        if (args['start_date'] != None and args['nights'] != None and args['rooms'] != None):
            #Parse the arguments into an object            

            actual_date = datetime.date.today()
            array_start_date = args['start_date'].split("_")
            if(len(array_start_date) != 3):
                return {'message': 'Date not correct '}, 400
            if(int(array_start_date[0]) < 0 or int(array_start_date[0]) > 31):
                return {'messages': f'Date (day : {array_start_date[0]}) not correct '}, 400
            if(int(array_start_date[1]) < 0 or int(array_start_date[1]) > 12):
                return {'messages': f'Date (month : {array_start_date[1]}) not correct '}, 400

            start_date = datetime.date(int(array_start_date[2]), int(array_start_date[1]), int(array_start_date[0]))
            nights = int(args['nights'])
            rooms = int(args['rooms'])

            # Verify if the request is correct
            if(start_date < actual_date):
                return {'message': 'Date not correct '}, 400
            if(nights <= 0):
                return {'message': 'Night can\'t be nul or negative'}, 400
            if(rooms <= 0 ):
                return {'message': 'Rooms can\'t be nul or negative'}, 400

            shelf_hotels = get_hotels_db()
            keys = list(shelf_hotels.keys())

            
            available_hotels = []
            total_rooms_bookings = {}
            for key in keys:
                if(int(shelf_hotels[key]['rooms']) >= rooms):
                    available_hotels.append(shelf_hotels[key])

            # Initiliasation du nombre de rooms réservé pour chaque hotel
            for available_hotel in available_hotels:
                print(available_hotel)
                total_rooms_bookings[available_hotel['identifier']] = int(available_hotel['rooms']) - rooms

            shelf_booking = booking.get_booking_db()
            keys = list(shelf_booking.keys())
            
            # Vérification des hotels disponible en fonction des dates de tous les bookings
            for key in keys:
                #print(shelf_booking[key])
                for available_hotel in available_hotels:
                    if(shelf_booking[key]['hotel_identifier'] == available_hotel["identifier"]):
                        # print("shelf_booking[key] :",shelf_booking[key]['name'])
                        array_booking_start_date = shelf_booking[key]['start_date'].split("_")
                        booking_start_date = datetime.date(int(array_booking_start_date[2]), int(array_booking_start_date[1]), int(array_booking_start_date[0]))
                        booking_nights = shelf_booking[key]['nights']
                        # Si la reservation est s'interpose sur le booking alors on soustrait le nombre de room
                        if(not self.delta_date(start_date,nights,booking_start_date) and not self.delta_date(booking_start_date, booking_nights, start_date)):
                            for i in range(len(available_hotels)):
                                if (available_hotels[i]['identifier'] == shelf_booking[key]["hotel_identifier"]):
                                    if( total_rooms_bookings[shelf_booking[key]["hotel_identifier"]] - int(shelf_booking[key]['rooms'])< 0):
                                        available_hotels.pop(i)
                                        break
                                    else:
                                        total_rooms_bookings[shelf_booking[key]["hotel_identifier"]] -=  int(shelf_booking[key]['rooms'])
                                    

            return {'data': available_hotels}, 200
    
        else:
            shelf = get_hotels_db()
            keys = list(shelf.keys())

            hotels = []

            for key in keys:
                hotels.append(shelf[key])

            return {'data': hotels}, 200
    
    def put(self):
        parser = reqparse.RequestParser()

        # Déparsage de tous les arguments
        parser.add_argument('name', required = True)
        parser.add_argument('rooms', required = True)

        #Parse the arguments into an object
        args = parser.parse_args()

        # Récupération de la base de donnée des hotels
        shelf = get_hotels_db()

        # Incrémentation de l'id
        id_book = str(len(shelf)+1)
        args['identifier'] = id_book

        shelf[args['identifier']] = args

        return {'data' : args}, 201
    
class Hotel(Resource):
    def get(self, identifier):
        shelf = get_hotels_db()

        if not identifier in shelf:
            return {'messages': 'Hotel not found'}, 404

        return {'data': shelf[identifier]}, 200

    def delete(self, identifier):
        shelf = get_hotels_db()

        if not identifier in shelf:
            return {'messages': 'Hotel not found'}, 404

        del shelf[identifier]

        return {''}, 204