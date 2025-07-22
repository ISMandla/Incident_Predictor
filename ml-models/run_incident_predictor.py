import psycopg2
import pandas as pd
import joblib
import time
import json
from kafka import KafkaConsumer
from threading import Thread
from sqlalchemy import create_engine

# --- Load Models ---
log_model = joblib.load("ml-models/log_classifier.pkl")
tfidf = joblib.load("ml-models/tfidf_vectorizer.pkl")
anomaly_model = joblib.load("ml-models/isolation_forest_model.pkl")

# --- PostgreSQL Setup ---
pg_conn = psycopg2.connect(
    dbname="incident_db",
    user="postgres",
    password="password",
    host="incident_postgres",
    port="5432"
)
pg_cursor = pg_conn.cursor()
pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS incident_predictions (
    id SERIAL PRIMARY KEY,
    source TEXT,
    original TEXT,
    prediction TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
pg_conn.commit()

# SQLAlchemy engine for pandas
engine = create_engine("postgresql+psycopg2://postgres:password@incident_postgres:5432/incident_db")

# --- Metric Anomaly Detection Thread ---
def anomaly_loop():
    last_checked_id = 0

    while True:
        try:
            query = f"SELECT id, cpu, memory, disk FROM system_metrics WHERE id > {last_checked_id} ORDER BY id ASC;"
            df = pd.read_sql(query, engine)

            if not df.empty:
                X = df[['cpu', 'memory', 'disk']]
                preds = anomaly_model.predict(X)

                for i, row in df.iterrows():
                    label = "Anomaly" if preds[i] == 1 else "Normal"
                    snapshot = f"CPU: {row['cpu']}, MEM: {row['memory']}, DISK: {row['disk']}"
                    print(f"[METRIC] ID {row['id']}: {label} - {snapshot}")
                    pg_cursor.execute(
                        "INSERT INTO incident_predictions (source, original, prediction) VALUES (%s, %s, %s)",
                        ("metric", snapshot, label)
                    )

                pg_conn.commit()
                last_checked_id = df['id'].max()
            else:
                print("[METRIC] No new data")

        except Exception as e:
            print("[ERROR][Metric Thread]", e)

        time.sleep(3)

# --- Log Classification Thread ---
def log_loop():
    try:
        consumer = KafkaConsumer(
            'logs',
            bootstrap_servers='kafka:9092',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        for message in consumer:
            try:
                log = message.value['log']
                vec = tfidf.transform([log])
                prediction = log_model.predict(vec)[0]
                print(f"[LOG] {log} → Label: {prediction}")
                pg_cursor.execute(
                    "INSERT INTO incident_predictions (source, original, prediction) VALUES (%s, %s, %s)",
                    ("log", log, prediction)
                )
                pg_conn.commit()
            except Exception as e:
                print("[ERROR][Log Thread] Failed to classify/insert:", e)

    except Exception as e:
        print("[ERROR] Kafka consumer failed:", e)

# --- Run Threads ---
Thread(target=anomaly_loop, daemon=True).start()
Thread(target=log_loop, daemon=True).start()

# --- Keep Main Thread Alive ---
while True:
    time.sleep(1)
