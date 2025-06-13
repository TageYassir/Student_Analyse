from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import dask.array as da
from dask_ml.preprocessing import StandardScaler
from dask_ml.linear_model import LinearRegression
from io import BytesIO
import pandas as pd
import numpy as np
import uvicorn
import joblib

from analysis import *
from backend.farePrediction import features

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/load-preview")
async def load_preview(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_parquet(BytesIO(content))
    return df.head(10).to_dict(orient="records")

@app.post("/clean")
async def clean(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_parquet(BytesIO(content))
    cleaned_df = clean_data(df)
    return {"message": "Data cleaned successfully!"}

@app.post("/enrich")
async def enrich(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_parquet(BytesIO(content))
    enriched_df = enrich_with_time_features(df)
    return {"message": "Data enriched successfully!"}

@app.post("/generate-plottrips")
async def generate_trips_plot(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_parquet(BytesIO(content))
    df_cleaned = clean_data(df)
    df_enriched = enrich_with_time_features(df_cleaned)
    plot_path = generate_trips_by_hour_plot(df_enriched)  # Function for trips plot
    plot_url = f"http://localhost:8000/{plot_path}"
    return {"plot_url": plot_url}

@app.post("/generate-plotprice")
async def generate_price_plot(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_parquet(BytesIO(content))
    df_cleaned = clean_data(df)
    df_enriched = enrich_with_time_features(df_cleaned)
    plot_path = generate_trips_price_by_hour_plot(df_enriched)  # Function for price plot
    plot_url = f"http://localhost:8000/{plot_path}"
    return {"plot_url": plot_url}


@app.post("/best-hour-work")
async def best_hour_work(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_parquet(BytesIO(content))  # Read parquet file
    df_cleaned = clean_data(df)  # Clean the data before processing
    best_hour_message = bestHourWork(df_cleaned)  # Get the best hour message
    return {"message": best_hour_message}  # Return the message in the response

# Global model and scaler (you can replace this with loading a saved model instead)
model = None
scaler = None

@app.on_event("startup")
async def load_model_and_scaler():
    global model, scaler
    model_path = "models/fare_model.pkl"
    scaler_path = "models/scaler.pkl"
    if os.path.exists(model_path) and os.path.exists(scaler_path):
        try:
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            print("Model and scaler loaded successfully.")
        except Exception as e:
            print(f"Error loading model or scaler: {e}")
    else:
        print("Model or scaler file not found. Skipping load.")


@app.post("/predict-price")
async def predict_price(
        distance: float = Form(...),
        passenger_count: int = Form(...),
        congestion_surcharge: float = Form(...),
        pickup_datetime: str = Form(...)  # Expecting ISO format string
):
    global model, scaler
    if model is None or scaler is None:
        return {"error": "Model not loaded yet."}

    # Parse datetime and extract features
    pickup_time = pd.to_datetime(pickup_datetime)
    hour_of_day = pickup_time.hour
    day_of_week = pickup_time.dayofweek
    month = pickup_time.month

    # Prepare input
    input_data = [[
        distance,
        passenger_count,
        congestion_surcharge,
        hour_of_day,
        day_of_week,
        month
    ]]

    input_scaled = scaler.transform(input_data)
    input_scaled_da = da.from_array(input_scaled, chunks=(1, len(features)))
    prediction = model.predict(input_scaled_da).compute()[0]
    return {"predicted_price": round(float(prediction), 2)}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)