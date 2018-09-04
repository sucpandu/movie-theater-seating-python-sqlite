'''
Created on Sep 2, 2018

@author: suchethapanduranga
'''

import sys
import unittest
import sqlite3
import pandas as pd
import numpy as np


def seat_info():
    conn = sqlite3.connect(sys.argv[1], check_same_thread=False)
    cur = conn.cursor()
    seatmap = cur.execute('''SELECT * FROM rows_cols''')
    for row in seatmap:
        row_id = row[0]
        cols = row[1]
        nrows = len(row_id)
    return row_id, cols, nrows


def reservation_info(infile):
    try:
        inp_df = pd.read_csv(infile, sep=" ", header=None)
        return len(inp_df)
    except pd.io.common.EmptyDataError:
        print("Empty File")

class read_res_request(object):
    def __init__(self, n, infile):
        self.n = n
        self.infile = infile

    def read(self):
        inp_df = pd.read_csv(infile, sep=" ", header=None)
        self.req_id = inp_df.loc[self.n, 0]                                 
        self.no_of_reservations = inp_df.loc[self.n, 1]  
        if self.no_of_reservations <= 0 or isinstance(self.no_of_reservations, str):
            print("Cannot Proceed: Number of Reservations entry is invalid")
            exit(0)
        return self.req_id, self.no_of_reservations

def create_seat_map():
    row_id, cols, nrows = seat_info()
    seats = np.zeros(shape=(nrows, cols))
    seat_id = np.array(seats, dtype=object)
    return seats, seat_id


def check_empty_seats(emp_seat_row):
    if sum(emp_seat_row) != 0:
        return True

def seat_tracker():
    emp_seat_row = []
    for i in range(nrows):
        emp_seat_row.append(cols)
    return emp_seat_row                                                

def update_seat_tracker(emp_seat_row, row):
    tmp = emp_seat_row[row]
    emp_seat_row[row] = tmp - 1
    return emp_seat_row                       

def available_seats(emp_seat_row):
    total_seats = sum(emp_seat_row)
    return total_seats                                            

def alphavalue_seats(row, col):
    row_number = row_id[row]
    seat_number = col + 1
    seat = row_number + str(seat_number)
    return seat, row_number, seat_number

def upd_db_seats(conn, seating):
    sql = ''' INSERT INTO seating (reservationID, row,seat) VALUES (? , ? ,? );'''
    cur = conn.cursor()
    try:
        cur.execute(sql, seating)       
    except sqlite3.IntegrityError:
        print("database Error: Seat already reserved to a customer")

def upd_db_metrics(conn, metrics):
    sql = ''' UPDATE metrics
              SET passengers_refused = ? ,
               passengers_separated = ?'''
    cur = conn.cursor()
    cur.execute(sql, metrics)  

def connect_db(db_file):
    try:
        conn = sqlite3.connect(database, check_same_thread=False)
        return conn
    except EnvironmentError as e:
        print(e)

def write_file(req_id, reserved_seats):
    with open(outfile, 'a') as out:
        out.write(req_id + " " + ','.join(reserved_seats))
        out.write("\n")
       
def _write_file_(req_id, errorMessage):
    with open(outfile, 'a') as out:
        out.write(req_id + " " + errorMessage)
        out.write("\n")
        
class group_case_one(object):

    def __init__(self, req_id, no_of_reservations):
        self.req_id = req_id
        self.no_of_reservations = no_of_reservations

    def group_case_one_allot(self):
        for i in range(nrows):
            for j in range(cols):
                if seats[i][j] == 0.0:
                    seats[i][j] = 1.0
                    seat_id[i][j] = self.req_id
                    update_seat_tracker(emp_seat_row, i)
                    seat, row_number, seat_number = alphavalue_seats(i, j)
                    conn = connect_db(database)
                    with conn:
                        upd_db_seats(conn, (self.req_id, row_number, seat_number))
                    return seat
                                        
class group_case_two(object):

    def __init__(self, req_id, no_of_reservations):
        self.req_id = req_id
        self.no_of_reservations = no_of_reservations

    def group_empty_row(self):
        for i in range(nrows):
            if emp_seat_row[i] >= self.no_of_reservations:                
                return i

    def group_seat_check(self):
        row = self.group_empty_row()
        temp = []
        for j in range(cols):    
            if seats[row][j] == 0:
                temp.append(j)
        return temp, row

    def seats_in_one_row(self):
        for i in range(nrows):
            return emp_seat_row[i] >= self.no_of_reservations
            
    def group_case_two_allot(self):
        temp, row = self.group_seat_check()
        alloted_seats = []
        seat_allocated = []
        for i in range(self.no_of_reservations):
            col = temp[i]
            seat_allocated.append(col)
            seats[row][col] = 1
            seat_id[row][col] = self.req_id
            update_seat_tracker(emp_seat_row, row)
            seat, row_number, seat_number = alphavalue_seats(row, col)
            alloted_seats.append(seat) 
            conn = connect_db(database)
            with conn:
                upd_db_seats(conn, (self.req_id, row_number, seat_number))        
        return alloted_seats

class group_case_three(object):

    def __init__(self, req_id, no_of_reservations):
        self.req_id = req_id
        self.no_of_reservations = no_of_reservations

    def group_case_three_allot(self):
        no_of_rows = self.no_of_reservations // cols
        remaining_seats = self.no_of_reservations % cols
        grouptwoObj = group_case_two(self.req_id, cols)
        for i in range(no_of_rows):
            grouptwoObj.group_case_two_allot()
        grouptwoObjnew = group_case_two(self.req_id, remaining_seats)
        grouptwoObjnew.group_case_two_allot()


def __main__(database, infile):
    reservations_discarded = 0
    reservations_split = 0
    total_reservations = reservation_info(infile)
    reserved_seats = []
    for n in range(total_reservations):
        readBookingObj = read_res_request(n, infile)
        req_id, no_of_reservations = readBookingObj.read()
        group_case_oneObj = group_case_one(req_id, no_of_reservations)
        gsctwoObj = group_case_two(req_id, no_of_reservations)
        group_case_threeObj = group_case_three(req_id, no_of_reservations)

        if check_empty_seats(emp_seat_row) and available_seats(emp_seat_row) >= no_of_reservations:
            if no_of_reservations == 1:
                seat = group_case_oneObj.group_case_one_allot()
                reserved_seats[0] = seat
                write_file(req_id, reserved_seats)

            elif no_of_reservations > 1 and no_of_reservations <= cols:
                flag = gsctwoObj.seats_in_one_row()

                if available_seats(emp_seat_row) > no_of_reservations and flag:
                    reserved_seats = gsctwoObj.group_case_two_allot()
                    write_file(req_id, reserved_seats)

                elif available_seats(emp_seat_row) >= no_of_reservations:
                    for res in range(no_of_reservations):
                        seat = group_case_oneObj.group_case_one_allot()
                        reserved_seats[0] = seat
                        write_file(req_id, reserved_seats)
                        reservations_split += 1

            elif no_of_reservations > cols:
                if available_seats(emp_seat_row) > no_of_reservations:
                    group_case_threeObj.group_case_three_allot()
                elif available_seats(emp_seat_row) == no_of_reservations:
                    for res in range(no_of_reservations):
                        seat = group_case_oneObj.group_case_one_allot()
                        reserved_seats[0] = seat
                        write_file(req_id, reserved_seats)
                        reservations_split += 1.0
                    
        elif available_seats(emp_seat_row) == 0:
            print("The theater is fully booked. Can't accomodate reservation", req_id)
            _write_file_(req_id, "The theater is fully booked. Can't accomodate reservation")
            reservations_discarded += no_of_reservations

        elif check_empty_seats(emp_seat_row) and available_seats(emp_seat_row) < no_of_reservations:
            print("Can't Accommodate the reservation", req_id)
            _write_file_(req_id, "The theater is fully booked. Can't accomodate reservation")
            reservations_discarded += no_of_reservations
            continue
        else:
            print("System Error")
            exit(0)

    print("Number of reservations split seats", reservations_split)
    print("Number of reservations refused seat confirmations", reservations_discarded)
    print("-----------------------Seat Matrix after reservations -----------------------")

    for i in range(nrows):
        rows = seat_id[i]
        print (rows)    
    return reservations_split, reservations_discarded
    
row_id, cols, nrows = seat_info()
seats, seat_id = create_seat_map()
emp_seat_row = seat_tracker()

if __name__ == '__main__':
    
    try:
        database = sys.argv[1]
        infile = sys.argv[2]
        outfile = sys.argv[3]
        print (outfile)
    except IndexError:
        print ('Please enter valid *.db, *.txt infile and outfile infiles')
        sys.exit()
        
    __main__(database, infile) 