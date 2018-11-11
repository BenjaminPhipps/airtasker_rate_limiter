from flask import Flask, request
from app import app
import unittest
from unittest.mock import patch
from rate_limiter import rate_limiter

class Rate_Limit_Tests(unittest.TestCase): 

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

#this is a simple testing function which ensures that the correct statuses and error messages are returned
#this test function assumes the period is max_amount and refill_amount are equal
#refill_period is in seconds
#given a max_amount/refill_amount and period to which the requests are limited
#max_amount and refill_period must be positive integers or floats
#request path must be a valid path with a correctly configured Rate_Limiter object as a decorator 
    def run_test(self, max_amount, refill_period, request_path): 
        user_1 = {'REMOTE_ADDR': '127.0.0.1'} #spoofing the ip addresses to test different users
        user_2 = {'REMOTE_ADDR': '127.0.0.2'}
        with patch('time.time') as time_now:        
            time_now.return_value = 0
            for i in range(int(max_amount)):
                result = self.app.get(request_path, environ_base=user_1) 
                self.assertEqual(result.status_code, 200)
            current_time = refill_period/2
            time_now.return_value = current_time
            result = self.app.get(request_path, environ_base=user_1) 
            self.assertEqual(result.status_code, 429)
            print("result is: ", result.data)
            wait_time = refill_period - current_time #real equation is (wait_time = period + last_refill  - current_time) but last_refill was at time 0
            expected = 'too soon, try again in '+str(wait_time)
            self.assertEqual(result.data, expected.encode("utf-8"))

            result = self.app.get(request_path, environ_base=user_2) 
            self.assertEqual(result.status_code, 200)

            time_now.return_value = refill_period + 1
            result = self.app.get(request_path, environ_base=user_1) 
            self.assertEqual(result.status_code, 200)

    def test_rate(self):
        self.run_test(1.0, 8,  '/test_1')
        self.run_test(2, 8,  '/test_2')
        self.run_test(5, 60,  '/test_3')
        self.run_test(100, 3600,  '/test_4')
        self.run_test(300, 86400,  '/test_5')

    #unit test for the refill function
    def test_refill(self):
        limiter = rate_limiter.Rate_Limiter(4.0, 2.0, 16.0)
        limiter.refill("user_id", 0.0)

        self.assertEqual(limiter.user_allowances["user_id"]['allowance'], 4.0)
        self.assertEqual(limiter.user_allowances["user_id"]['last_refill'], 0.0)

        limiter.user_allowances["user_id"]['allowance'] = 0.0
        limiter.refill("user_id", 15.0)

        self.assertEqual(limiter.user_allowances["user_id"]['allowance'], 0.0)
        self.assertEqual(limiter.user_allowances["user_id"]['last_refill'], 0.0)

        limiter.refill("user_id", 16.0)

        self.assertEqual(limiter.user_allowances["user_id"]['allowance'], 2.0)
        self.assertEqual(limiter.user_allowances["user_id"]['last_refill'], 16.0)        



if __name__ == '__main__':
    unittest.main()