import os
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the dataset
data_path = 'data/traffic_data.csv'
if not os.path.exists(data_path):
    raise FileNotFoundError("Run yolo_detection.py first to generate the dataset!")

df = pd.read_csv("data/traffic_data.csv")
print(df.columns)
print(df.head())

# Features and Target
X = df[['vehicle_count']]
y = pd.cut(
    df["vehicle_count"],
    bins=[-1, 10, 25, 100],
    labels=[0, 1, 2]
).astype(int)

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Predictive Model
print("Training Traffic Density Prediction Model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%")

# Save Model
os.makedirs('model', exist_ok=True)
with open('model/traffic_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model successfully saved to model/traffic_model.pkl")