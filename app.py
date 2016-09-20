import argparse
import json
import logging
import socket
from threading import Thread

from flask import Flask


app = Flask(__name__)

count = 0

@app.route("/")
def ahahah():
    logging.debug('serving count: {}'.format(count))
    return str(count)


logging.basicConfig(level=logging.DEBUG)

producer = Thread(target = app.run, daemon = True, kwargs = {'host': '0.0.0.0'})

try:
    producer.start() producer.join()
except KeyboardInterrupt:
    pass
