import pandas as pd
import xgboost as xgb
import numpy as np
import json
from sklearn.metrics import accuracy_score

# Load the model
model = xgb.XGBClassifier()
model.load_model("major_delay_model.json")

# Load the threshold
with open("threshold_config.json", "r") as f:
    config = json.load(f)
threshold = config["threshold"]

# Load dataset
df = pd.read_csv("dec24toapril25WOUTLIERS.csv")

# Simulate "live" data
mock_live = df.sample(10, random_state=67)
X_live = mock_live.drop(columns=["Arrival Delay"])
y_true = mock_live["Arrival Delay"].apply(lambda x: 1 if x >= 25 else 0)

# Predict probabilities
probs = model.predict_proba(X_live)[:, 1]

# Predict labels with threshold
y_pred = (probs >= threshold).astype(int)

# Classify risk levels
def classify_risk(p):
    if p < 0.4:
        return "Low"
    elif p < 0.7:
        return "Medium"
    else:
        return "High"

risk_levels = [classify_risk(p) for p in probs]

# Display results
for i, (p, risk) in enumerate(zip(probs, risk_levels)):
    print(f"Flight {i+1}:")
    print(f"  Predicted probability of major delay: {p:.2f}")
    print(f"  Risk Level: {risk}")
    print(f"  Predicted: {y_pred[i]} | Actual: {y_true.iloc[i]}")
    print("-" * 30)

# Accuracy
accuracy = accuracy_score(y_true, y_pred)
print(f"\n🔎 Accuracy on mock live sample: {accuracy:.2f}")
