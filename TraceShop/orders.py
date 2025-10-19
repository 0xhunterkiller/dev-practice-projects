import redis
import json
import time
from pymongo import MongoClient
import logging
import sys
import os

log = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)
log.setLevel(logging.DEBUG)

# MongoDB Connection
client = MongoClient(os.environ.get('MONGO_URI'))
db = client['product']
tcoll = db['transactions']

def process_next_item(queue_name='ordersQ'):
    r = redis.Redis(host=os.environ.get('REDIS_HOST'), port=6379, db=0)
    while True:
        transaction = json.loads(r.blpop(queue_name)[1])
        if transaction:
            log.info(f"Order Processing: {transaction['tid']}")
            time.sleep(2)
            filter_query = {'tid': transaction['tid']}
            update_query = {'$set': {'status': 'order complete'}}
            result = tcoll.update_many(filter_query, update_query)
            log.info(f"Delivered: {transaction['tid']}")

if __name__ == "__main__":
    queue_name = 'ordersQ'
    process_next_item(queue_name)