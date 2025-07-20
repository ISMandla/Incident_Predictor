
import time, random, json
from kafka import KafkaProducer

logs = [
    "INFO: User logged in",
    "WARNING: High memory usage detected",
    "ERROR: Database connection failed",
    "INFO: Scheduled backup completed",
    "ERROR: Disk read error",
    "WARNING: CPU spike detected"
]

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:
    log_entry = {"log": random.choice(logs), "timestamp": time.time()}
    producer.send('system_logs', log_entry)
    print(f"Sent log: {log_entry}")
    time.sleep(3)
