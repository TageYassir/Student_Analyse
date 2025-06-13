import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import joblib
import pandas as pd
import os

from starlette.middleware.cors import CORSMiddleware
# Import your plot generator here
from plot_generator import generate_all_plots

app = FastAPI(title="Student Graduation Predictor + Plots")

model = joblib.load("model/student_gb_model.pkl")

origins = [
    "http://localhost:5173",  # your React app origin
    # You can add more origins here if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] to allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

plot_dir = "individual_plots"
upload_dir = "uploaded_data"
os.makedirs(plot_dir, exist_ok=True)
os.makedirs(upload_dir, exist_ok=True)

app.mount("/plots", StaticFiles(directory=plot_dir), name="plots")

class StudentInput(BaseModel):
    Mark: float
    Scholarship: int
    Gender: str
    School: str
    Specialty: str
    Validated_Semesters: int
    Repeated_Semesters: int
    Failed_Semesters: int

@app.post("/predict")
def predict_graduation(data: StudentInput):
    input_df = pd.DataFrame([data.dict()])
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]
    return {
        "Graduated_Prediction": bool(prediction),
        "Probability": round(probability, 4)
    }

@app.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    save_path = os.path.join(upload_dir, file.filename)
    with open(save_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    return {"status": "File uploaded successfully", "filename": file.filename}

@app.get("/generate-plots")
def generate_plots():
    # Use the latest uploaded CSV if exists, else default path
    files = [f for f in os.listdir(upload_dir) if f.endswith(".csv")]
    if files:
        csv_path = os.path.join(upload_dir, sorted(files)[-1])  # Last uploaded file
    else:
        csv_path = r"backend\generated_data_v3_1.csv"

    generate_all_plots(csv_path)  # This should generate PNGs inside individual_plots

    return {
        "status": "✅ Plots generated successfully.",
        "plot_urls": [f"/plots/{fname}" for fname in os.listdir(plot_dir) if fname.endswith(".png")]
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)