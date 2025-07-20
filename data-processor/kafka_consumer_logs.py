
from kafka import KafkaConsumer
import json
import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["incident_db"]
log_collection = db["system_logs"]

consumer = KafkaConsumer(
    'system_logs',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    data = message.value
    log_collection.insert_one(data)
    print("Stored log:", data)
