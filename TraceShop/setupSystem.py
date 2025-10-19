from pymongo import MongoClient
import os

products = [
  {"id": 1, "name": "Widget A", "price": 20.99},
  {"id": 2, "name": "Gizmo B", "price": 29.99},
  {"id": 3, "name": "Thingamajig C", "price": 14.99},
  {"id": 4, "name": "Doodad D", "price": 9.99},
  {"id": 5, "name": "Whatchamacallit E", "price": 39.99}
]

import redis

# Connect to Redis
r = redis.Redis(host=os.environ.get('REDIS_HOST'), port=6379, db=0)

def setupSystem():
  # Delete all keys in the current database
  r.flushdb()
  # Populate MongoDB
  client = MongoClient(os.environ.get('MONGO_URI'))
  db = client['product']
  for cname in ['forsale','transactions']:
    collection = db[cname]
    collection.drop()
  collection = db['forsale']
  collection.insert_many(products)