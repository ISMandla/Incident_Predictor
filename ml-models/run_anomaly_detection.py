import pandas as pd
import joblib
import time
from sqlalchemy import create_engine

# Load trained model
model = joblib.load("isolation_forest_model.pkl")

# Create SQLAlchemy engine
engine = create_engine("postgresql+psycopg2://postgres:password@localhost:5432/incident_db")

last_checked_id = 0

count = 0
while True:
    try:
        # Fetch new rows
        query = f"SELECT id, cpu, memory, disk FROM system_metrics WHERE id > {last_checked_id} ORDER BY id ASC;"
        df = pd.read_sql(query, engine)

        if not df.empty:
            X = df[['cpu', 'memory', 'disk']]
            preds = model.predict(X)

            for i, row in df.iterrows():
                label = "Anomaly" if preds[i] == -1 else "Normal"
                print(f"ID {row['id']}: {label} - CPU: {row['cpu']} MEM: {row['memory']} DISK: {row['disk']}")
                count += 1
                print(count)

            last_checked_id = df['id'].max()
    except Exception as e:
        print("[ERROR] Anomaly detection loop:", e)

    time.sleep(3)  # check every 3 seconds
