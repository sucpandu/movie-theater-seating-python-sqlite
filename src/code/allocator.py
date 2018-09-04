'''
Created on Sep 2, 2018

@author: suchethapanduranga
'''

import sys
import unittest
from helpers import seat_info, create_seat_map, seat_tracker, update_seat_tracker, alphavalue_seats
from dbutility import db_utility
import pandas as pd

                                                                                                                
#  class read_res_request()                                                                                            
#     This class has function read() which reads the input text file and convert it into a pandas dataframe.       
#                                                                                                                     

class read_res_request(object):     

    def __init__(self, n, infile):
        self.n = n
        self.infile = infile

    def read(self, infile):
        inp_df = pd.read_csv(infile, sep=" ", header=None)
        self.req_id = inp_df.loc[self.n, 0]                                 
        self.no_of_reservations = inp_df.loc[self.n, 1]  
        if self.no_of_reservations <= 0 or isinstance(self.no_of_reservations, str):
            print("Cannot Proceed: Number of Reservations entry is invalid")
            exit(0)
        return self.req_id, self.no_of_reservations

#   group_case_one() 
#       Case1: methods for reserving seats to a      
#       customer (reservationId) with a requisition only for One ticket
    
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
                    #emp_seat_row.sort(reverse=True)
                    update_seat_tracker(emp_seat_row, i)
                    seat = alphavalue_seats(i, j)
                    update_db(database, self.req_id, seat)
                    return seat

                                        
#   group_case_two() 
#       Case2: methods for reserving seats to a 
#       customer (reservationId) with total ticket count 
#       less than or equal to the number of seats in a single row
  
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
            if emp_seat_row[i] >= self.no_of_reservations:
                return True
            
    def group_case_two_allot(self):
        temp, row = self.group_seat_check()
        alloted_seats = []
        seat_allocated = []
        for i in range(self.no_of_reservations):
            col = temp[i]
            seat_allocated.append(col)
            seats[row][col] = 1
            seat_id[row][col] = self.req_id
            #emp_seat_row.sort(reverse=True)  #remove
            update_seat_tracker(emp_seat_row, row)
            seat = alphavalue_seats(row, col)
            alloted_seats.append(seat) 
            update_db(database, self.req_id, seat)    
        return alloted_seats


#   group_case_three() 
#       Case2: methods for reserving seats to a 
#       customer (reservationId) with total ticket count 
#       more than the number of seats in a single row
 
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

#   utility functions
#       reservation_info()
#          validates the information in the input text file 
#          and returns the number of reservations
#       write_file()
#          write the assigned seats corresponding to a 
#          particular reqId to the output file 
#       update_db()
#            update the reserved seats information to the database
#        
 
def reservation_info(infile):
    try:
        inp_df = pd.read_csv(infile, sep=" ", header=None)
        return len(inp_df)
    except pd.io.common.EmptyDataError:
        print("Empty File")

        
def write_file(outfile, req_id, assignments):
    with open(outfile, 'a') as out:
        if isinstance(assignments, list):
            out.write(req_id + " " + ','.join(assignments))
            out.write("\n")
        else:
            out.write(req_id + " " + assignments)
            out.write("\n")

            
def update_db(database, req_id, seat):
    dbObj = db_utility()
    conn = dbObj.connect_db(database)
    with conn:
        dbObj.upd_db_seats(conn, (req_id, seat))   
        
        
#   The seat assignment algorithm works the following way:
#
#0. Requested seats are allocated adjacently in a row with maximum number of free seats.
#
#1. If the number of seats requested is 1, the first empty seat that can be found will be assigned.
#
#2. If the number of seats requested is less than the no. of seats in each row, 
#   a row which has enough empty seats to accommodate these reservations will be 
#   tracked and the empty seats will be assigned to this request. 
#
#3. When the number of seats requested exceeds the number of seats in a row, 
#   appropriate splits are performed to make sure maximum possible alloted seats 
#   are together and remaining alloted seats using Case 1 algorithm.
#
#4. If the number of seats requested are more than the free seats available, 
#   an empty list of seats is returned.
#
#   After each allocation, seat matrix, empty seat tracker and database are being updated.

def seat_allocator(req_id, no_of_reservations):
    
    reserved_seats = []
    
    group_case_oneObj = group_case_one(req_id, no_of_reservations)
    gsctwoObj = group_case_two(req_id, no_of_reservations)
    group_case_threeObj = group_case_three(req_id, no_of_reservations)
    
    if sum(emp_seat_row) and sum(emp_seat_row) >= no_of_reservations:
        
        # case1: no_of_reservations == 1 
        if no_of_reservations == 1:
            seat = group_case_oneObj.group_case_one_allot()
            reserved_seats.append(seat)
            
            
        # case2: no_of_reservations < no.of seats in a row 
        elif no_of_reservations > 1 and no_of_reservations <= cols:
            flag = gsctwoObj.seats_in_one_row()
            
            if sum(emp_seat_row) > no_of_reservations and flag:
                reserved_seats = gsctwoObj.group_case_two_allot()
                

            elif sum(emp_seat_row) >= no_of_reservations:
                for res in range(no_of_reservations):
                    seat = group_case_oneObj.group_case_one_allot()
                    reserved_seats.append(seat)
                    
                    
        # case3: no_of_reservations > no.of seats in a row
        elif no_of_reservations > cols:
            if sum(emp_seat_row) > no_of_reservations:
                group_case_threeObj.group_case_three_allot()
            elif sum(emp_seat_row) == no_of_reservations:
                for res in range(no_of_reservations):
                    seat = group_case_oneObj.group_case_one_allot()
                    reserved_seats.append(seat)
                    
        
        write_file(outfile, req_id, reserved_seats)                        
    
    elif sum(emp_seat_row) == 0:
        write_file(outfile, req_id, "The theater is fully booked. Can't accommodate anymore reservations")
        
    elif sum(emp_seat_row) and sum(emp_seat_row) < no_of_reservations:
        write_file(outfile, req_id, "Insufficient Seats! Seats left in the screen  " + str(sum(emp_seat_row)))
        # continue
    else:
        print("System Error")
        exit(0)
    
    return reserved_seats
        
         
#  Main method takes two inputs, 
#  1. database to fetch the information from 
#  2. input text file containing the reservation ID
#  It browses through each record in the input file and then class objects are used to call appropriate methods. 

def __main__(database, infile):
        
    total_reservations = reservation_info(infile)
    reserved_total = 0  
    for n in range(total_reservations):
        
        readBookingObj = read_res_request(n, infile)
        req_id, no_of_reservations = readBookingObj.read(infile)
        
        reserved_seats = seat_allocator(req_id, no_of_reservations)
        reserved_total = reserved_total + (len(reserved_seats))
    
    return reserved_total

row_id, cols, nrows = seat_info()
seats, seat_id = create_seat_map()
emp_seat_row = seat_tracker()

#----- Test Suite for asserting the correctness of data -----#
    
class test_total_seats(unittest.TestCase):

    def __init__(self, testname, test_database, test_filename):
        super(test_total_seats, self).__init__(testname)
        self.database = test_database
        self.filename = test_filename


    def test_total_reservations(self):
        reserved_total_test = __main__(self.database, self.filename)
        self.assertEqual(reserved_total_test, 5)
        
        
    def test_seat_info(self):  
        row_id, cols, nrows = seat_info()
        self.assertEqual(nrows,10, msg='reading incorrect seat row information')
        self.assertEqual(cols, 10, msg='reading incorrect seat column information')
        
    def test_seat_allocate(self):
        reserved_seats_test = seat_allocator('R001', 2)
        self.assertEqual(len(reserved_seats_test), 2)
        self.assertEqual(reserved_seats_test[0], 'A1')
        self.assertEqual(reserved_seats_test[1], 'A2')
        self.assertEqual(reserved_seats_test[2], 'A3')
        self.assertEqual(reserved_seats_test[3], 'A4')   
        
if __name__ == '__main__':
    try:
        database = sys.argv[1]
        infile = sys.argv[2]
        outfile = sys.argv[3]  
        
        
        __main__(database, infile)
        
        print("-----------------------Seat Matrix after reservations -----------------------")
    
        for i in range(nrows):
            rows = seat_id[i]
            print (rows)
            
        print("-------------------Testing Data-------------------")
        suite = unittest.TestSuite()
        suite.addTest(test_total_seats("test_total_reservations",database,infile))
        suite.addTest(test_total_seats("test_seat_info",database,infile))
        suite.addTest(test_total_seats("test_seat_allocate", database,infile))
        unittest.TextTestRunner().run(suite)
               
    except IndexError:
        print ('Please enter valid *.db, *.txt infile and outfile infiles')
        sys.exit()
