
import pandas as pd
import psycopg2
from sklearn.ensemble import IsolationForest
import joblib

conn = psycopg2.connect(
    dbname="incident_db",
    user="postgres",
    password="password",
    host="incident_postgres",
    port="5432"
)

query = "SELECT cpu, memory, disk FROM system_metrics"

df = pd.read_sql_query(query, conn)
conn.close()

X = df[['cpu', 'memory', 'disk']]
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
model.fit(X)
joblib.dump(model, "isolation_forest_model.pkl")
print("Isolation Forest model saved.")
