import dask.dataframe as dd
from dask_ml.model_selection import train_test_split
from dask_ml.preprocessing import StandardScaler
from dask_ml.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib
import os
import pandas as pd

from backend.analysis import clean_data

def enrich_model(df):
    """Extract time-based features from tpep_pickup_datetime"""
    df = df.copy()
    df['hour_of_day'] = df['tpep_pickup_datetime'].dt.hour
    df['day_of_week'] = df['tpep_pickup_datetime'].dt.dayofweek  # Monday=0, Sunday=6
    df['month'] = df['tpep_pickup_datetime'].dt.month
    return df

# === Load Data ===
df_input = dd.read_parquet(r"C:\Users\fftt7\PycharmProjects\taxiNewYork\backend\uploads\yellow_tripdata_2024-01.parquet")

# === Convert to pandas if needed ===
if isinstance(df_input, dd.DataFrame):
    df_input = df_input.compute()

# === Clean and Enrich ===
df = clean_data(df_input)
df = enrich_model(df)

# === Convert back to Dask ===
df = dd.from_pandas(df, npartitions=4)

# === Filter Data ===
required_columns = ['trip_distance', 'passenger_count', 'congestion_surcharge', 'fare_amount']
df = df[required_columns + ['hour_of_day', 'day_of_week', 'month']].dropna()
df = df[(df['trip_distance'] > 0) & (df['fare_amount'] > 0)]
df = df[(df['fare_amount'] < 200) & (df['trip_distance'] < 50)]

# === Features and Target ===
features = ['trip_distance', 'passenger_count', 'congestion_surcharge',
            'hour_of_day', 'day_of_week', 'month']
X = df[features]
y = df['fare_amount']

# === Convert to Dask arrays ===
X = X.to_dask_array(lengths=True)
y = y.to_dask_array(lengths=True)

# === Split ===
X_train, X_val, y_train, y_val = train_test_split(X, y, train_size=0.8, random_state=42, shuffle=True)

# === Scaling ===
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

# === Train Model ===
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# === Predict & Evaluate ===
y_pred = model.predict(X_val_scaled).compute()
y_val = y_val.compute()
rmse = np.sqrt(mean_squared_error(y_val, y_pred))

print("RMSE:", rmse)

# === Save Model and Scaler ===
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/fare_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")