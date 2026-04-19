import pandas as pd
import time
import json
import warnings
import requests
from datetime import datetime
from sklearn.ensemble import IsolationForest

warnings.filterwarnings("ignore", category=UserWarning)

LOKI_URL = "http://127.0.0.1:3100/loki/api/v1/push"

def push_to_loki(payload):

    timestamp_ns = str(time.time_ns())
    
    loki_payload = {
        "streams": [
            {
                "stream": {
                    "job": "capstone_ml_sensors", 
                    "location": payload["location"]
                },
                "values": [
                    [timestamp_ns, json.dumps(payload)] 
                ]
            }
        ]
    }
    
    try:

        response = requests.post(LOKI_URL, json=loki_payload)

        if response.status_code == 204:
            pass 
        else:
            print(f"❌ LOKI REJECTED DATA: Status {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("🚨 CRITICAL: Cannot reach Loki! Make sure Docker is running on port 3100.")
    except Exception as e:
        print(f"🚨 ERROR: {e}")

def train_and_run_live_spooler(csv_filepath):
    print(f"Loading data from '{csv_filepath}'...")
    
    try:
        df = pd.read_csv(csv_filepath)
    except FileNotFoundError:
        print(f"🚨 ERROR: Cannot find {csv_filepath}. Make sure it is in the same folder as this script!")
        return
        
    features = ['Temperature', 'Humidity', 'AQI', 'Pressure']

    print("Training Location-Aware ML Models (Isolation Forest)...")
    models = {}
    locations = df['Location'].unique()
    
    for loc in locations:
        loc_data = df[df['Location'] == loc][features]

        model = IsolationForest(contamination=0.02, random_state=42)
        model.fit(loc_data)
        models[loc] = model
        print(f" - Trained baseline for {loc}")

    print("\n✅ Models Trained! Starting Live Feed to Loki...\n")
    print("-" * 65)
  
    for index, row in df.iterrows():
        current_loc = row['Location']
        current_data = pd.DataFrame([[row['Temperature'], row['Humidity'], row['AQI'], row['Pressure']]], columns=features)

        prediction = models[current_loc].predict(current_data)[0]
        raw_score = models[current_loc].decision_function(current_data)[0]

        grafana_anomaly_score = max(0, min(100, (0.5 - raw_score) * 100))
        
        is_anomaly = True if prediction == -1 else False
  
        if is_anomaly:
            print(f"\n🚨 ML ALERT DETECTED at {current_loc}! Score: {grafana_anomaly_score:.1f}")
            print(f"   Pushing Threat to Grafana Dashboard... 🚨\n")
        else:
            print(f"Sent normal reading for {current_loc}...")
            
        payload = {
            "timestamp": datetime.now().isoformat(),
            "location": current_loc,
            "temperature": float(row['Temperature']),
            "humidity": float(row['Humidity']),
            "aqi": float(row['AQI']),
            "pressure": float(row['Pressure']),
            "ml_anomaly_score": round(grafana_anomaly_score, 2),
            "is_anomaly": is_anomaly
        }

        push_to_loki(payload)

        time.sleep(1) 

if __name__ == "__main__":
    train_and_run_live_spooler('env_data.csv')