# airtasker_rate_limiter

How to use:

-Import the package
e.g. "from rate_limiter import rate_limiter"

-Construct an object from the class Rate_Limiter, constructor arguments are max_amount, refill_amount and refill_period (in that order)
e.g. "rate_limit_1 = rate_limiter.Rate_Limiter(1.0, 1.0, 8.0)"

-Use the object to decorate a flask route function
e.g. """
@app.route('/test_1', endpoint='test_handler_1')
@rate_limit_1
def test_handler_1():
    return 'Hello, World!'
"""


Algorithm choice:
I chose to use the token bucket algorithm, I made this choice because it seemed to be an industry standard while being reasonably simple and performant

Dependencies:
- This package depends on Python Flask and will only work when decorating a Flask route. I made the choice to do this because Flask is very widely used and I found it difficult to create a totally generalizable rate limiter that was both easy to use and returned proper response objects. Despite this it would be reasonably simple to adapt this solution to a different web framework.

- This package also depends upon the Python 3 standard library (threading and time)
