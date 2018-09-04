'''
Created on Sep 3, 2018

@author: suchethapanduranga
'''
import sys
import pandas as pd
import numpy as np
import sqlite3

#  seat_info()                                                                                                     
#     This function reads rows and column info from the seat_config table in the database                             
#     row_id identifies the row in the movie theater by an alphanumeric value (A,B ..)
#  seat_tracker()                                                                                           
#     This function will create a list to read number of total empty seats in a row                           
#                                                                                                                     
#  update_seat_tracker()                                                                                           
#     This function will update the total number of empty seats remaining while any booking is made
#
#   alphavalue_seats()
#     This function computes the seat number from matrix index to alphanumeric identifiers (A1, A2 ..) 
# 
#   create_seat_map()
#     This function reads the seating configuration of the movie theater from database file, 
#     based on which it generates a seat map i.e creating numpy matrix of given rows and cols                            
#     values: 0 is empty seat and 1 is occupied seat                                                                    

def seat_info():
    conn = sqlite3.connect(sys.argv[1], check_same_thread=False)
    cur = conn.cursor()
    seatmap = cur.execute('''SELECT * FROM seat_config''')
    for row in seatmap:
        row_id = row[0]
        cols = row[1]
        nrows = len(row_id)
    return row_id, cols, nrows

def create_seat_map():
    row_id, cols, nrows = seat_info()
    seats = np.zeros(shape=(nrows, cols))
    seat_id = np.array(seats, dtype=object)
    return seats, seat_id

def seat_tracker():
    row_id, cols, nrows = seat_info()
    emp_seat_row = []
    for i in range(nrows):
        emp_seat_row.append(cols)
    return emp_seat_row                                                

def update_seat_tracker(emp_seat_row, row):
    tmp = emp_seat_row[row]
    emp_seat_row[row] = tmp - 1
    return emp_seat_row                       

def alphavalue_seats(row, col):
    row_id, cols, nrows = seat_info()
    row_number = row_id[row]
    seat_number = col + 1
    seat = row_number + str(seat_number)
    return seat