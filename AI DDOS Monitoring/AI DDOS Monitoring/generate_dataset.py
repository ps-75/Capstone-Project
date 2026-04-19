import csv
import random
import numpy as np

TOTAL_SECONDS = 10000

print(" Generating Enterprise Time-Series Dataset for Autoencoder Training...")

with open('traffic_dataset.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['RPS', 'Unique_IPs', 'Response_Time_ms'])
    
    for i in range(TOTAL_SECONDS):
        rps = int(np.random.normal(5, 2))
        if rps < 1: rps = 1
        
        unique_ips = rps - random.randint(0, 1)
        if unique_ips < 1: unique_ips = 1
            
        response_time = int(np.random.normal(40, 5))
        
        if i % 1000 > 950:  
            rps = int(np.random.normal(30, 5)) 
            unique_ips = int(rps * 0.9)  
            response_time = int(np.random.normal(60, 10))
            
        writer.writerow([rps, unique_ips, response_time])

print("✅ 'traffic_dataset.csv' created successfully!")
print("Your dataset contains 10,000 rows of multi-dimensional traffic logs.")