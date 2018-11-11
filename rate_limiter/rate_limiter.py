import time
import threading 
import flask
from flask import request


class Rate_Limiter():
    def __init__(self, max_amount, refill_amount, refill_period):
        self.max_amount = max_amount # Max amount of requests that a user can accumulate when not making requests
        self.refill_period = refill_period # How often the user gets new a new allowance of requests to make in seconds
        self.refill_amount = refill_amount # How many requests the user gets every refill_period
        self.user_allowances = {} # The dictionary storing users current allowances and when they last had they allowance refilled
        self.lock = threading.Lock() # A simple lock in order to make this class threadsafe, 
                                     # this could cause scaling issues but only one python thread can execute at any one time regardless of this lock

    #refills the bucket of a given user at a given time
    #if a bucket for the user does not exist, it is created
    def refill(self, user_id, current_time): 
        if user_id not in self.user_allowances.keys():
            self.user_allowances[user_id] = {'allowance': self.max_amount, 'last_refill': current_time}

        refill_count = int((current_time - self.user_allowances[user_id]['last_refill'] ) / self.refill_period)
        self.user_allowances[user_id]['allowance'] = min(
            self.max_amount,
            self.user_allowances[user_id]['allowance'] + refill_count * self.refill_amount
        )
        self.user_allowances[user_id]['last_refill'] = min(
            current_time, 
            self.user_allowances[user_id]['last_refill'] + refill_count * self.refill_period
        )

    #this is the actual rate limiter function, it is written as a decorator for ease of use
    def __call__(self, func):
        def rate_limiter_wrapper(*args, **kwargs):
            user_id = str(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
            self.lock.acquire()
            current_time = time.time()
            self.refill(user_id, current_time)
 
            if (self.user_allowances[user_id]['allowance'] < 1.0):
                self.lock.release()
                wait_time = self.refill_period + self.user_allowances[user_id]['last_refill']  - current_time
                message = "too soon, try again in " + str(wait_time)
                resp = flask.make_response(message, 429)
                return resp 
            else:
                self.user_allowances[user_id]['allowance'] -= 1.0
                self.user_allowances[user_id]['last_refill'] = current_time
                self.lock.release()
                return func()
        return rate_limiter_wrapper


if __name__ == "__main__":
    print("in main of rate_limiter.py")
    pass
