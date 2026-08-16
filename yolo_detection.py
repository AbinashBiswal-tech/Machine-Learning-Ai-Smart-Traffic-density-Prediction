import cv2
import csv
import os
from ultralytics import YOLO

# ---------------------------------------
# FILE PATHS
# ---------------------------------------

VIDEO_PATH = "traffic_video.mp4"
CSV_PATH = "data/traffic_data.csv"
MODEL_PATH = "yolov8n.pt"

# ---------------------------------------
# CREATE DATA FOLDER
# ---------------------------------------

os.makedirs("data", exist_ok=True)

# ---------------------------------------
# LOAD YOLOv8 MODEL
# ---------------------------------------

print("Loading YOLOv8 model...")

model = YOLO(MODEL_PATH)

# ---------------------------------------
# VEHICLE CLASSES
# COCO:
# 2 = car
# 3 = motorcycle
# 5 = bus
# 7 = truck
# ---------------------------------------

VEHICLE_CLASSES = [2, 3, 5, 7]

# ---------------------------------------
# OPEN TRAFFIC VIDEO
# ---------------------------------------

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("ERROR: Could not open traffic_video.mp4")
    exit()

print("Video opened successfully.")
print("Starting YOLO vehicle detection...")

# ---------------------------------------
# CREATE / OVERWRITE CSV
# ---------------------------------------

with open(CSV_PATH, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "step",
        "vehicle_count",
        "traffic_density"
    ])

    step = 0

    # ---------------------------------------
    # PROCESS VIDEO FRAME BY FRAME
    # ---------------------------------------

    while True:

        ret, frame = cap.read()

        # Stop when video ends
        if not ret:
            print("Video ended.")
            break

        # -----------------------------------
        # YOLO DETECTION
        # -----------------------------------

        results = model(
            frame,
            conf=0.40,
            verbose=False
        )

        vehicle_count = 0

        # -----------------------------------
        # COUNT VEHICLES
        # -----------------------------------

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                class_id = int(box.cls[0])

                if class_id in VEHICLE_CLASSES:
                    vehicle_count += 1

        # -----------------------------------
        # TRAFFIC DENSITY
        # -----------------------------------

        if vehicle_count <= 10:

            traffic_density = "Low"

        elif vehicle_count <= 25:

            traffic_density = "Medium"

        else:

            traffic_density = "High"

        # -----------------------------------
        # SAVE DATA TO CSV
        # -----------------------------------

        writer.writerow([
            step,
            vehicle_count,
            traffic_density
        ])

        file.flush()

        # -----------------------------------
        # SHOW RESULT IN TERMINAL
        # -----------------------------------

        print(
            f"Step {step}: "
            f"{vehicle_count} vehicles - "
            f"{traffic_density} density"
        )

        step += 1

# ---------------------------------------
# RELEASE VIDEO
# ---------------------------------------

cap.release()

print("--------------------------------")
print("YOLO DATA COLLECTION COMPLETE")
print("--------------------------------")
print("CSV file:", CSV_PATH)
print("Total frames processed:", step)

