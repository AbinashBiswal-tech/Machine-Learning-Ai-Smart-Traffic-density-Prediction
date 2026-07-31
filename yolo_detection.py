import os
import csv
import time
import random
import cv2
from ultralytics import YOLO


# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)
csv_path = 'data/traffic_data.csv'

# Initialize CSV file with headers if it doesn't exist
if not os.path.exists(csv_path):
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Hour', 'Minute', 'Vehicle_Count', 'Traffic_Density'])

# Load YOLO
model = YOLO('yolov8n.pt')

print("Starting video processing and data logging...")
cap=cv2.VideoCapture("traffic_video.mp4")

# Simulating data collection over a loop (mimicking video frames)
# In production, replace the loop with: cap = cv2.VideoCapture('simulation_video.mp4')
for i in range(1000):
    current_time = time.localtime()
    hour = current_time.tm_hour
    minute = current_time.tm_min
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
    
    # Simulating YOLO detection count (replace with actual len(boxes) from frame)
    # Simulate realistic traffic patterns

    ret, frame= cap.read()

    if not ret:
        print("Video ended")
        break

    results = model(frame)

    vehicle_count = 0

    for box in results[0].boxes:
        cls = int(box.cls[0])

    # car, motorcycle, bus, truck
    if cls in [2, 3, 5, 7]:
        vehicle_count += 1

    # Calculate Density Categorization
    density = 0 if vehicle_count < 5 else (1 if vehicle_count <= 10 else 2) # 0: Low, 1: Medium, 2: High

    # Append data to csv
    with open(csv_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, hour, minute, vehicle_count, density])
        
    time.sleep(0.1) # Simulate time passing quickly for dataset generation

cap.release()
print("Dataset path:", os.path.abspath(csv_path))
print("Data collection complete!")