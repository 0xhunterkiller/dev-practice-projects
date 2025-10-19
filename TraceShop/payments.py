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

def process_next_item(queue_name='paymentsQ'):
    r = redis.Redis(host=os.environ.get('REDIS_HOST'), port=6379, db=0)
    while True:
        transaction = json.loads(r.blpop(queue_name)[1])
        if transaction:
            log.info(f"Processing transaction: {transaction['tid']}")
            time.sleep(2)
            r.rpush('ordersQ',json.dumps(transaction,default=str))
            filter_query = {'tid': transaction['tid']}
            update_query = {'$set': {'status': 'payment complete'}}
            result = tcoll.update_many(filter_query, update_query)
            log.info(f"Processing Complete, moved to Orders: {transaction['tid']}")

if __name__ == "__main__":
    queue_name = 'paymentsQ'
    process_next_item(queue_name)
