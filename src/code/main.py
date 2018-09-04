'''
Created on Sep 3, 2018

@author: suchethapanduranga
'''
import sys
import unittest
from allocator import *
from dbutility import db_utility
import pandas as pd

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

        if sum(emp_seat_row) and sum(emp_seat_row) >= no_of_reservations:
            if no_of_reservations == 1:
                seat = group_case_oneObj.group_case_one_allot()
                reserved_seats[0] = seat
                write_file(req_id, reserved_seats)

            elif no_of_reservations > 1 and no_of_reservations <= cols:
                flag = gsctwoObj.seats_in_one_row()

                if sum(emp_seat_row) > no_of_reservations and flag:
                    reserved_seats = gsctwoObj.group_case_two_allot()
                    write_file(req_id, reserved_seats)

                elif sum(emp_seat_row) >= no_of_reservations:
                    for res in range(no_of_reservations):
                        seat = group_case_oneObj.group_case_one_allot()
                        reserved_seats[0] = seat
                        write_file(req_id, reserved_seats)
                        reservations_split += 1

            elif no_of_reservations > cols:
                if sum(emp_seat_row) > no_of_reservations:
                    group_case_threeObj.group_case_three_allot()
                elif sum(emp_seat_row) == no_of_reservations:
                    for res in range(no_of_reservations):
                        seat = group_case_oneObj.group_case_one_allot()
                        reserved_seats[0] = seat
                        write_file(req_id, reserved_seats)
                        reservations_split += 1.0
                    
        elif sum(emp_seat_row) == 0:
            print("The theater is fully booked. Can't accommodate reservation", req_id)
            _write_file_(req_id, "The theater is fully booked. Can't accommodate reservation")
            reservations_discarded += no_of_reservations

        elif sum(emp_seat_row) and sum(emp_seat_row) < no_of_reservations:
            print("Can't Accommodate the reservation", req_id)
            _write_file_(req_id, "The theater is fully booked. Can't accommodate reservation")
            reservations_discarded += no_of_reservations
            continue
        else:
            print("System Error")
            exit(0)

    def write_file(req_id, reserved_seats):
        with open(outfile, 'a') as out:
            out.write(req_id + " " + ','.join(reserved_seats))
            out.write("\n")
       
    def _write_file_(req_id, errorMessage):
        with open(outfile, 'a') as out:
            out.write(req_id + " " + errorMessage)
            out.write("\n")
        
    print("Number of reservations refused seat confirmations", reservations_discarded)
    print("-----------------------Seat Matrix after reservations -----------------------")

    for i in range(nrows):
        rows = seat_id[i]
        print (rows)    
    return reservations_split, reservations_discarded
    

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