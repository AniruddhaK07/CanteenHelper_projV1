from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
import uvicorn
import os

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and encoder
try:
    model = joblib.load('canteen_model.pkl')
    le = joblib.load('dish_encoder.pkl')
    dishes = le.classes_
except Exception as e:
    print(f"Error loading model: {e}")
    model, le, dishes = None, None, []

@app.get("/api/predict")
def predict_day(day_of_week: int = None):
    if model is None:
        return {"error": "Model not loaded. Please train the model first."}
        
    if day_of_week is None:
        day_of_week = datetime.now().weekday()
        
    # Predict for each hour (8 to 17) and each dish
    hours = list(range(8, 18))
    predictions = []
    
    for hour in hours:
        for dish in dishes:
            dish_encoded = le.transform([dish])[0]
            # Predict demand
            qty = model.predict([[hour, day_of_week, dish_encoded]])[0]
            predictions.append({
                "hour": hour,
                "dish": dish,
                "predicted_quantity": round(qty, 2)
            })
            
    # Calculate total predicted demand per hour to find peak hours
    hour_totals = {}
    for p in predictions:
        h = p['hour']
        hour_totals[h] = hour_totals.get(h, 0) + p['predicted_quantity']
        
    # Sort hours by demand
    peak_hours = sorted(hour_totals.items(), key=lambda x: x[1], reverse=True)[:3]
    formatted_peak_hours = [{"hour": f"{h}:00 - {h+1}:00", "total_demand": round(v)} for h, v in peak_hours]
    
    # Aggregate demand per dish for the whole day to recommend prep
    dish_totals = {}
    for p in predictions:
        d = p['dish']
        dish_totals[d] = dish_totals.get(d, 0) + p['predicted_quantity']
        
    top_dishes = sorted(dish_totals.items(), key=lambda x: x[1], reverse=True)[:4]
    formatted_top_dishes = [{"dish": d, "predicted_demand": round(v)} for d, v in top_dishes]
    
    return {
        "day_of_week": day_of_week,
        "peak_hours": formatted_peak_hours,
        "prep_recommendations": formatted_top_dishes,
        "all_predictions": predictions
    }

# Create frontend directory if not exists
if not os.path.exists("frontend"):
    os.makedirs("frontend")

# Mount frontend
if os.path.exists("frontend/index.html"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return {"message": "API is running. Frontend not found."}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)