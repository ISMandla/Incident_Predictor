import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import pymongo


client = pymongo.MongoClient("mongodb://incident_mongo:27017/")

db = client["incident_db"]
collection = db["system_logs"]

cursor = collection.find({"log": {"$exists": True}, "label": {"$exists": True}})
logs_data = list(cursor)
client.close()


data = pd.DataFrame(logs_data)
X = data['log']
y = data['label']

X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


tfidf = TfidfVectorizer()
X_train = tfidf.fit_transform(X_train_raw)
X_test = tfidf.transform(X_test_raw)

model = LogisticRegression()
model.fit(X_train, y_train)

joblib.dump(model, "log_classifier.pkl")
joblib.dump(tfidf, "tfidf_vectorizer.pkl")

print("✅ Log classifier and TF-IDF vectorizer saved successfully.")

