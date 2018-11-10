import time
from flask import Flask
from flask import request
from app import app
import unittest
from unittest.mock import patch

class Rate_Limit_Tests(unittest.TestCase): 

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

#this is a simple testing function which ensures that the correct statuses are returned 
#given a rate and period to which the requests are limited
#rate can be a float but is makes more sense as an integer
#period must be given as a float or an error will be thrown
#request path must be a valid path with a correctly configured Rate_Limiter object as a decorator 
    def run_test(self, rate, period, request_path): 
        with patch('time.time') as time_now:        
            time_now.return_value = 0
            for i in range(int(rate)):
                result = self.app.get(request_path) 
                self.assertEqual(result.status_code, 200)
                #print("result is: ", result.data)

            time_now.return_value = period/2
            result = self.app.get(request_path)
            self.assertEqual(result.status_code, 429)
            print("result is: ", result.data)
            expected = 'too soon, try again in '+str(period)
            self.assertEqual(result.data, expected.encode("utf-8"))

            time_now.return_value = period/2 + 1
            result = self.app.get(request_path)
            self.assertEqual(result.status_code, 200)

    def test_rate(self):
        pass
        #self.run_test(1.0, 8.0,  '/test_1')
        #self.run_test(2, 8.0,  '/test_2')
        #self.run_test(5, 60.0,  '/test_3')
        #self.run_test(100, 3600.0,  '/test_4')
        #self.run_test(300, 86400.0,  '/test_5')

    def test_rate_2(self):
        request_path = '/test_2'
        result = self.app.get(request_path) 
        self.assertEqual(result.status_code, 200)
        result = self.app.get(request_path) 
        self.assertEqual(result.status_code, 200)
        time.sleep(4)
        result = self.app.get(request_path) 
        self.assertEqual(result.status_code, 429)



if __name__ == '__main__':
    unittest.main()