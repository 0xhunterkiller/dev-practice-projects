from flask import Flask, jsonify, request
from pymongo import MongoClient
import json
import sys
import redis
import logging
import uuid
import setupSystem
import os

setupSystem.setupSystem()

app = Flask(__name__)

def fetchProducts(pid:int = -1):
    if pid > 0:
        # Check cache
        cacheres = cache.hget('product',pid)
        if cacheres:
            log.debug(f"cache hit for id: {pid}")
            answer = json.loads(cacheres)
        else:
            found = collection.find({"id":pid})
            sfound = json.dumps(list(found),default=str)
            answer = json.loads(sfound)
            if answer:

                cache.hset('product',pid,sfound)
    if pid < 0:
        found = collection.find({})
        answer = json.loads(json.dumps(list(found),default=str))
    return answer


# GET products
@app.route('/api/products',methods=['GET'])
def allProducts():
    return fetchProducts(-1)

# GET products
@app.route('/api/product/<int:id>',methods=['GET'])
def productById(id):
    res = fetchProducts(id)
    if res:
        return res
    else:
        return "Sorry, product with that ID was not found", 404

# GET buy
@app.route('/api/buy/<int:id>')
def buyProduct(id):
    # Push product to payment-queue
    log.info("Payment process starting")
    product = fetchProducts(id)
    if product:
        tid = str(uuid.uuid4())
        transaction = {
            "tid": tid,
            "product":product[0]['id'],
            "status": "processing"
        }
        transactions = db['transactions']
        transactions.insert_one(transaction)
        q.rpush('paymentsQ',json.dumps(transaction,default=str))
        return str(tid) + "\n"
    else:
        return "Sorry, product with that ID was not found\n", 404

if __name__ == "__main__":
    log = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    log.addHandler(handler)
    log.setLevel(logging.DEBUG)
    log.debug("Logger Initialised")

    # MongoDB Connection
    client = MongoClient(os.environ.get('MONGO_URI'))
    db = client['product']
    collection = db['forsale']
    log.info("Connected to MONGO")

    # Cache Connection
    cache = redis.Redis(host=os.environ.get('REDIS_HOST'), port=6379, db=0)
    log.info("Connected to CACHE")

    # Queue Connections
    q = redis.Redis(host=os.environ.get('REDIS_HOST'), port=6379, db=0)
    log.info("Connected to QUEUES")

    app.run(debug=False)