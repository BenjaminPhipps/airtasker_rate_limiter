# The task is to produce a rate-limiting module that stops a particular requestor from making too many http requests within a particular period of time.

# The module should expose a method that keeps track of requests and limits it such that a requester can only make 100 requests per hour. 
#After the limit has been reached, return a 429 with the text "Rate limit exceeded. Try again in #{n} seconds".

# Although you are only required to implement the strategy described above, it should be easy to extend the rate limiting module to take on different rate-limiting strategies.

# How you do this is up to you. Think about how easy your rate limiter will be to maintain and control. Write what you consider to be production-quality code, with comments and tests if and when you consider them necessary.

# import time




import time
import threading #us this
import flask
#from flask import current_app as app
from flask import request


class UserDecorators():
    def __init__(self, rate, period):
        self.rate = rate; # unit: messages
        self.period  = period; # unit: seconds
        self.allowance = rate; # unit: messages
        #self.last_check = time.time();
        self.rate_over_period = self.rate / self.period
        self.user_allowances = {}
        #print(self.last_check)
        print("init done")

    def get_user_allowance(self, user_id):
        if user_id not in self.user_allowances.keys():
            self.user_allowances[user_id] = {'allowance': self.allowance, 'last_check': time.time()}
        return self.user_allowances[user_id]

    def set_user_allowance(self, user_id, allowance, last_check):
        self.user_allowances[user_id]['allowance'] = allowance
        print("new allowance is: ", self.user_allowances[user_id]['allowance'])
        self.user_allowances[user_id]['last_check'] = last_check
        print("last checked: ", self.user_allowances[user_id]['last_check'])


    def __call__(self, func):
        def run_function_if_green(*args, **kwargs):
            #print("user_id")
            #rate_over_period = self.rate / self.period
            user_id = str(request.environ.get('HTTP_X_REAL_IP', request.remote_addr))
            #user_id = "blah"
            print("user_id is: ", user_id)
            user_allowance = self.get_user_allowance(user_id)
            last_check = user_allowance['last_check']
            current = time.time()
            time_passed = current - last_check
            print("initial allowance is: ", user_allowance['allowance'])
            allowance = (time_passed * self.rate_over_period) + user_allowance['allowance']
            print("allowance is ", allowance)
            print("rate is ", self.rate)
            if (allowance > self.rate):
                print("throttleing now")
                allowance = self.rate; #throttle
            if (allowance < 1.0):
                print("equation is ", (1.0 - allowance), self.rate_over_period)
                wait_time = (1.0 - allowance) / self.rate_over_period
                message = "too soon, try again in " + str(wait_time)
                #return {"message":message, "status": 429}
                #print("too soon, try again in ", wait_time)
                #return  jsonify({"message": message}), 429
                # with self.app.app_context():
                #resp = flask.make_response({"message": message}, 429)
                resp = flask.make_response(message, 429)
                return resp 
                #return 429
            else:
                #self.allowance -= 1.0;
                allowance -= 1.0
                self.set_user_allowance(user_id, allowance, current)
                return func()
        return run_function_if_green



if __name__ == "__main__":
    print("in main of rate_limiter.py")
    pass
