
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

df = pd.read_csv("system_metrics_sample.csv")
X = df[['cpu', 'memory', 'disk']]
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
model.fit(X)
joblib.dump(model, "isolation_forest_model.pkl")
print("Isolation Forest model saved.")
