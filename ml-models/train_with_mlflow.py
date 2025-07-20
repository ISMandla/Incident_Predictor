
import pandas as pd
from sklearn.ensemble import IsolationForest
import mlflow
import mlflow.sklearn

df = pd.read_csv("system_metrics_sample.csv")
X = df[['cpu', 'memory', 'disk']]

mlflow.set_experiment("Anomaly Detection")
with mlflow.start_run():
    model = IsolationForest(n_estimators=100, contamination=0.05)
    model.fit(X)
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("contamination", 0.05)
    mlflow.sklearn.log_model(model, "model")
    print("Model logged to MLflow")
