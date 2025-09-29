import pandas as pd
import xgboost as xgb
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
model = joblib.load('./ml_models/2.1m.pkl')

df = pd.read_csv('testDATA.csv')

# Optional: drop any non-feature columns if necessary (like Arrival Delay if it’s accidentally present)
scheduled_arrival = df["Scheduled Arrival"]
actual_arrival_delay = df["Arrival Delay"]
actual_arrival_time = scheduled_arrival + actual_arrival_delay

# Prepare features (drop target)
X_new = df.drop(columns=["Arrival Delay"])

# Predict
predicted_delay = model.predict(X_new)
predicted_arrival_time = scheduled_arrival + predicted_delay

# Combine for comparison
comparison_df = pd.DataFrame({
    "Scheduled Arrival": scheduled_arrival,
    "Predicted Delay": predicted_delay,
    "Actual Delay": actual_arrival_delay,
    "Predicted Arrival Time": predicted_arrival_time,
    "Actual Arrival Time": actual_arrival_time
})

# Save or preview
print(comparison_df.head(10))
mae = mean_absolute_error(actual_arrival_delay, predicted_delay)
rmse = np.sqrt(mean_squared_error(actual_arrival_delay, predicted_delay))

# Output metrics
print(f"MAE: {mae:.2f} minutes")
print(f"RMSE: {rmse:.2f} minutes")
comparison_df.to_csv("arrival_predictions.csv", index=False)

