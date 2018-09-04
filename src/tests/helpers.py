'''
Created on Sep 3, 2018

@author: suchethapanduranga
'''

import unittest
from code.helpers import alphavalue_seats, seat_info

class test_total_seats(unittest.TestCase):

    """def __init__(self, testname, test_database, test_filename):
        super(test_total_seats, self).__init__(testname)
        self.database = test_database
        self.filename = test_filename"""
        
    def test_seat_info(self):  
        row_id, cols, nrows = seat_info()
        self.assertEqual(nrows,10, msg='reading incorrect seat row information')
        self.assertEqual(cols, 10, msg='reading incorrect seat column information')
        
    def test_alphavalue_seats(self): 
        self.assertEqual(alphavalue_seats(0,0), 'A1')
        self.assertEqual(alphavalue_seats(10,8), 'J8')
        self.assertEqual(alphavalue_seats(5,4), 'E4')
        self.assertEqual(alphavalue_seats(28,28), 'AB28')
        
    
if __name__ == "__main__":
    unittest.main()
    
    