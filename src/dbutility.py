'''
Created on Sep 3, 2018

@author: suchethapanduranga
'''
import sys
import sqlite3

class db_utility(object):
    
    """set of database helper functions"""
    
    def upd_db_seats(self, conn, reservations):
        sql = ''' INSERT INTO reservations (reservationID, row,seat) VALUES (? , ? ,? );'''
        cur = conn.cursor()
        try:
            cur.execute(sql, reservations)       
        except sqlite3.IntegrityError:
            print("database Error: Seat already reserved to a customer")
    
    def connect_db(self, database):
        try:
            conn = sqlite3.connect(database, check_same_thread=False)
            return conn
        except EnvironmentError as e:
            print(e)
            