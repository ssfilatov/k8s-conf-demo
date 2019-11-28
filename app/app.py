import logging
import os
import time

from flask import Flask, request


app = Flask(__name__)


@app.route('/handler')
def handler():
    return 'OK'


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
    app.run(host='0.0.0.0', port=os.getenv("HTTP_PORT", 8081))

