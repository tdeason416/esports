from kafka import KafkaConsumer
import json
import ast
import pymongo
from pymongo import MongoClient

KAFKA_TOPIC_NAME='mlb_games'
MONGO_DB_NAME='mlb_db'

def insert_record(record):
    client = MongoClient('localhost', 27017)
    db = client[MONGO_DB_NAME]
    record_id = db.mlb_collection.insert_one(record).inserted_id
    print(record_id)
    
#consumer = KafkaConsumer(bootstrap_servers='localhost:9092', auto_offset_reset='earliest', consumer_timeout_ms=1000)
consumer = KafkaConsumer(bootstrap_servers='localhost:9092', group_id='mlb_reader', consumer_timeout_ms=1000)
consumer.subscribe([KAFKA_TOPIC_NAME])

for message in consumer:
    data = ast.literal_eval(message.value)
    insert_record(data)

