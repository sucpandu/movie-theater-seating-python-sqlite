'''
Created on Sep 3, 2018

@author: suchethapanduranga
'''
import unittest
from code.allocator import seat_allocator

class test_total_seats(unittest.TestCase):

    """def __init__(self, testname, test_database, test_filename):
        super(test_total_seats, self).__init__(testname)
        self.database = test_database
        self.filename = test_filename"""

    """def test_total_reservations(self):
        reserved_total_test = __main__(self.database, self.filename)
        self.assertEqual(reserved_total_test, 5)"""
            
    def test_seat_allocate(self):
        reserved_seats_test = seat_allocator('R001', 2)
        self.assertEqual(len(reserved_seats_test), 2)
        self.assertEqual(reserved_seats_test[0], 'A1')
        self.assertEqual(reserved_seats_test[1], 'A2')
        self.assertEqual(reserved_seats_test[2], 'A3')
        self.assertEqual(reserved_seats_test[3], 'A4')   
        