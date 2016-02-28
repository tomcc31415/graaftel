import argparse
import json
import logging
import socket
import threading
from threading import Thread

from flask import Flask

from proton.handlers import MessagingHandler
from proton.reactor import Container


app = Flask(__name__)

count = 0

class Tel(MessagingHandler):
    def __init__(self, address):
        super(Tel, self).__init__()
        self._address = address
        
    def on_start(self, event):
        logging.info('receive from: {}'.format(self._address))
        event.container.create_receiver(self._address)

    def on_message(self, event):
        global count
        logging.debug('received message: {}'.format(event.message.body))
        count += 1

@app.route("/")
def ahahah():
    logging.debug('serving count: {}'.format(count))
    return str(count)

            
parser = argparse.ArgumentParser(
    description='Count messages from an AMQP address and serve to HTTP clients')
parser.add_argument('--address', help='the AMQP address, e.g. amqp://username:password@localhost:5672/sparkhara',
                    required=True)

args = parser.parse_args()

logging.basicConfig(level=logging.DEBUG)

receiver = Thread(target = Container(Tel(args.address)).run, daemon = True)
producer = Thread(target = app.run, daemon = True, kwargs = {'host': '0.0.0.0'})

try:
    receiver.start(), producer.start(), receiver.join(), producer.join()
except KeyboardInterrupt:
    pass
