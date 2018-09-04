'''
Created on Sep 3, 2018

@author: suchethapanduranga
'''
import sys
import pandas as pd
import numpy as np
import sqlite3


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
    return seat, row_number, seat_number
