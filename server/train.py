import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import xgboost as xgb
import shap


# Parameters
params = 21.58  # millions of samples (for model naming)

# Load and split data
df = pd.read_csv("january22->april25.csv")
X = df.drop(columns=["Arrival Delay"])
y = df["Arrival Delay"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = xgb.XGBRegressor(
    n_estimators=1200,        # Try bumping this a bit
    learning_rate=0.15,       # Slightly slower learning to reduce overshooting
    max_depth=7,              # Slightly more complex trees
    subsample=0.8,            # Helps reduce overfitting
    colsample_bytree=0.8,     # Random feature subsampling
    random_state=1,
    objective='reg:squarederror'
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"MAE: {mae:.2f}")
print(f"RMSE: {rmse:.2f}")

# Save model
joblib.dump(model, f'./ml_models/{params}m_mae{mae:.2f}.pkl')
print("Model saved successfully.")



# Plot SHAP values
sample = X_train.sample(1000, random_state=42)
explainer = shap.Explainer(model, sample)
shap_values = explainer(sample)

# Summary plot (global feature importance)

xgb.plot_importance(model)
plt.title("XGBoost Feature Importance")
plt.tight_layout()
plt.savefig("xgb_feature_importance.png")
plt.clf()

shap.summary_plot(shap_values, sample)
plt.title("SHAP Summary Plot")
plt.tight_layout()
plt.savefig("shap_summary_plot.png")