'''
Created on Sep 3, 2018

@author: suchethapanduranga
'''
import sys
import sqlite3

#  Database functions 
#
#  upd_db_seats()                                                                                                  #
#     This function updates the reservation Id and assigned seats to the database (table reservations)                      #
#                                                                                                                     #                                                                                                             #
#  connect_db()                                                                                             #
#     This function establishes a database connection   

class db_utility(object): 
    
    """set of database helper functions"""
       
    def upd_db_seats(self, conn, reservations):
        sql = ''' INSERT INTO reservations (reservationID, seat) VALUES (? , ? );'''
        cur = conn.cursor()
        try:
            cur.execute(sql, reservations)       
        except sqlite3.IntegrityError:
            print("Database error: an attempt is being made to alter an already booked reservation")
            pass
    
    def connect_db(self, database):
        try:
            conn = sqlite3.connect(database, check_same_thread=False)
            return conn
        except EnvironmentError as e:
            print(e)
            