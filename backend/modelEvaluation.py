import numpy as np
from dask_glm.utils import mean_squared_error
from dask_ml.ensemble import RandomForestRegressor

from backend.farePrediction import X_train_scaled, y_train, X_val_scaled, y_val

# Train Random Forest Model
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train_scaled, y_train)

# Predict and evaluate Random Forest Model
y_pred_rf = rf.predict(X_val_scaled).compute()
rmse_rf = np.sqrt(mean_squared_error(y_val.compute(), y_pred_rf))

print(f"Random Forest RMSE: {rmse_rf:.4f}")
