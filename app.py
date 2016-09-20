import argparse
import json
import logging
import socket
from threading import Thread

from flask import Flask

from operator import add
from collections import Counter

from pyspark import SparkContext
from pyspark.streaming import StreamingContext


app = Flask(__name__)


words = Counter()

@app.route("/")
def ahahah():
    logging.debug('serving counts...')
    return str(words.most_common(10))

def consumer():
    def process(time, rdd):
        global words
        words += Counter(dict(rdd.collect()))

    sc = SparkContext(appName='graaftel')
    ssc = StreamingContext(sc, 5)

    lines = ssc.socketTextStream('localhost', 2016)
    counts = lines.flatMap(lambda line: line.lower().split()) \
                  .map(lambda word: (word, 1)) \
                  .reduceByKey(add)
    counts.foreachRDD(process)

    ssc.start()
    ssc.awaitTermination()

logging.basicConfig(level=logging.DEBUG)

receiver = Thread(target = consumer)
producer = Thread(target = app.run, kwargs = {'host': '0.0.0.0'})

receiver.daemon = True
producer.daemon = True
try:
    receiver.start(), producer.start()
    receiver.join(), producer.join()
except KeyboardInterrupt:
    pass
