
from kafka import KafkaConsumer
import json
import psycopg2

conn = psycopg2.connect(
    dbname="incident_db",
    user="postgres",
    password="password",
    host="incident_postgres",
    port="5432"
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS system_metrics (
    id SERIAL PRIMARY KEY,
    cpu FLOAT,
    memory FLOAT,
    disk FLOAT,
    timestamp DOUBLE PRECISION
)
""")
conn.commit()

consumer = KafkaConsumer(
    'system_metrics',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    data = message.value
    cursor.execute("INSERT INTO system_metrics (cpu, memory, disk, timestamp) VALUES (%s, %s, %s, %s)",
                   (data['cpu'], data['memory'], data['disk'], data['timestamp']))
    conn.commit()
    print("Stored metric:", data)
