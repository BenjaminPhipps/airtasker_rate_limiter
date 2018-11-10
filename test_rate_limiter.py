from rate_limiter import rate_limiter
import time
from flask import Flask
from flask import request


app = Flask(__name__)


curr_dec = rate_limiter.UserDecorators(1.0, 8.0) #make these kwargs??

# @curr_dec
# def test_api():
#     print('successful call, return 200')

@app.route('/')
@curr_dec
def test_api():
    print("in the business now")
    return 'Hello, World!'

#request.environ.get('HTTP_X_REAL_IP', request.remote_addr)



def main():
    print("started")
    app.run()
    # with app.app_context():
    #     test_api("user_id")
    #     test_api("user_id")
    #     test_api("user_id_2")
    #     time.sleep(7)
    #     test_api("user_id")
    #     print("done")


if __name__ == "__main__":
    main()