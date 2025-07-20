import psycopg2
import time
import yagmail
import schedule

# Set this to True to print instead of send
TEST_MODE = False

# Setup PostgreSQL connection
conn = psycopg2.connect(
    dbname="incident_db",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Set up email sender using yagmail (uses Gmail)
yag = yagmail.SMTP("ishaan.mandla@gmail.com", "ziyf traf hrow ydbi")

# Store the last seen ID
last_seen_id = 0

def check_for_alerts():
    global last_seen_id
    cursor.execute("""
        SELECT id, source, original, prediction, timestamp
        FROM incident_predictions
        WHERE id > %s
        ORDER BY id ASC
    """, (last_seen_id,))
    
    rows = cursor.fetchall()
    for row in rows:
        id, source, original, prediction, ts = row
        if source == 'metric' and prediction == 'Anomaly':
            send_alert(f"[ALERT - METRIC] {original} at {ts}")
        elif source == 'log' and prediction.lower() in ['error', 'critical', 'fatal']:
            send_alert(f"[ALERT - LOG] {original} classified as {prediction} at {ts}")
        last_seen_id = id

def send_alert(message):
    print("🚨 Sending alert:", message)
    if not TEST_MODE:
        yag.send(
            to="ishaan.mandla@gmail.com",
            subject="🚨 Incident Alert!",
            contents=message
        )

# Run check every 10 seconds
schedule.every(10).seconds.do(check_for_alerts)

print("📡 Alert engine started.")
while True:
    schedule.run_pending()
    time.sleep(1)
