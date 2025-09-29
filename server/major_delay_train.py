import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import xgboost as xgb
import numpy as np
import json

# Load dataset
df = pd.read_csv("1yearfrommay24WOUTLIERS.csv")

# Label target: 1 if major delay (30+ min), else 0
df["Major Delay"] = df["Arrival Delay"].apply(lambda x: 1 if x >= 25 else 0)

# Drop original target
X = df.drop(columns=["Arrival Delay", "Major Delay"])
y = df["Major Delay"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Handle class imbalance
pos = sum(y_train)
neg = len(y_train) - pos
scale_pos_weight = neg / pos

# Create XGBoost classifier
model = xgb.XGBClassifier(
    n_estimators=500,
    learning_rate=0.1,
    max_depth=6,
    scale_pos_weight=scale_pos_weight,
    objective='binary:logistic',
    eval_metric='logloss',
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# Predict probabilities
y_proba = model.predict_proba(X_test)[:, 1]

# Fixed threshold
threshold = 0.60
y_pred = (y_proba >= threshold).astype(int)

# Evaluate
print(f"Threshold: {threshold}")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("First 10 predicted probabilities:", y_proba[:10])

# Save model
model.save_model("6.79m_major_delay_model.json")
print("Model saved as major_delay_model.json")

# Save threshold
with open("threshold_config.json", "w") as f:
    json.dump({"threshold": threshold}, f)
print("Threshold saved as threshold_config.json")
