from rate_limiter import rate_limiter
import time
from flask import Flask
from flask import request


app = Flask(__name__)


rate_limit_1 = rate_limiter.Rate_Limiter(1.0, 8.0) #make these kwargs??
rate_limit_2 = rate_limiter.Rate_Limiter(2.0, 8.0) #make these kwargs??
rate_limit_3 = rate_limiter.Rate_Limiter(5.0, 60.0) #make these kwargs??
rate_limit_4 = rate_limiter.Rate_Limiter(100.0, 60.0 * 60.0) #make these kwargs??
rate_limit_5 = rate_limiter.Rate_Limiter(300.0, 60.0 * 60.0 * 24.0)


@app.route('/test_1', endpoint='test_handler_1')
@rate_limit_1
def test_handler_1():
    print("in the business now")
    return 'Hello, World!'


@app.route('/test_2', endpoint='test_handler_2')
@rate_limit_2
def test_handler_2():
    print("in the business now")
    return 'Hello, World!'


@app.route('/test_3', endpoint='test_handler_3')
@rate_limit_3
def test_handler_3():
    print("in the business now")
    return 'Hello, World!'

@app.route('/test_4', endpoint='test_handler_4')
@rate_limit_4
def test_handler_4():
    print("in the business now")
    return 'Hello, World!'

@app.route('/test_5', endpoint='test_handler_5')
@rate_limit_5
def test_handler_5():
    print("in the business now")
    return 'Hello, World!'


def main():
    print("started")
    app.run()


if __name__ == "__main__":
    main()