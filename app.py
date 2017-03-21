import os
import logging
import socket
from threading import Thread
import string

from flask import Flask, request, jsonify, render_template

from operator import add
from collections import Counter

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

from stop_words import get_stop_words


app = Flask(__name__)

stop_words = get_stop_words('nl')
stop_words += (u'[', u']', u'')

words = Counter()

@app.route("/")
def ahahah():
    logging.debug('serving counts...')
    top = words.most_common(int(request.args.get('n') or 10))
    return render_template('index.html',
                           categories=map(lambda x: x[0], top),
                           data=map(lambda x: x[1], top))
#    return jsonify(dict(top))

@app.route("/updatedata")
def dataonly():
    logging.debug('serving data...')
    top = words.most_common(int(request.args.get('n') or 10))
    data=map(lambda x: x[1], top)
    categories = map(lambda x: x[0], top)
    data.insert(0, "counts")
    return jsonify({"categories": categories, "data": [data]})


def consumer():
    def process(time, rdd):
        global words
        words += Counter(dict(rdd.collect()))

    sc = SparkContext(appName='graafteldev')
    ssc = StreamingContext(sc, 5)

    lines = ssc.socketTextStream(os.getenv('PRODUCER_SERVICE_HOST', 'localhost'),
                                 int(os.getenv('PRODUCER_SERVICE_PORT', 8080)))
    counts = lines.flatMap(lambda line: line.encode('ascii', 'ignore').lower().split()) \
                  .map(lambda word: word.translate(None, string.punctuation)) \
                  .filter(lambda word: word not in stop_words) \
                  .map(lambda word: (word, 1)) \
                  .reduceByKey(add)
    counts.foreachRDD(process)

    ssc.start()
    ssc.awaitTermination()

#logging.basicConfig(level=logging.DEBUG)

receiver = Thread(target = consumer)
producer = Thread(target = app.run, kwargs = {'host': '0.0.0.0', 'port': 8080})

receiver.daemon = True
producer.daemon = True
try:
    receiver.start(), producer.start()
    while True:
        receiver.join(10), producer.join(10)
except KeyboardInterrupt:
    pass
