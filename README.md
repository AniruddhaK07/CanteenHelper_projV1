# Canteen Peak Time & Dish Predictor
Canteen waiting times are frustrating.
This project uses Machine Learning to predict peak canteen hours and recommend which dishes to prepare in advance based on historical POS data. By anticipating demand, canteen staff can reduce student wait times during busy college hours.

## Project Structure & Files

The project is organized as follows:
- `datasets/`: Contains the simulated historical POS data (`canteen_pos_data.csv`).
- `app.py`: FastAPI backend that serves predictions.
- `train_model.py`: Script to train the Random Forest model.
- `generate_data.py`: Script to generate mock data for simulation.
- `canteen_model.pkl` & `dish_encoder.pkl`: Trained model and label encoder artifacts.
- `frontend/`: Contains the dashboard UI (`index.html`).
- `.gitignore`: Specifies files and folders to be ignored by Git (e.g., `__pycache__`, models, datasets).

## Project Architecture & Flow

1. **Data Collection (Simulation)**
   * **Script**: `generate_data.py`
   * **Process**: Since real canteen POS data wasn't available, we simulate 60 days of transactional data. The mock data includes `Date`, `Time`, `Dish`, and `Quantity`. It's engineered to reflect real-world college patterns (lunch peaks around 12-2 PM, snack peaks around 4-5 PM).
   * **Output**: `datasets/canteen_pos_data.csv`

2. **Data Analysis & Model Training**
   * **Script**: `train_model.py`
   * **Process**: 
     - Loads the CSV and engineers temporal features: `Hour` and `DayOfWeek`.
     - Aggregates the total quantity ordered per dish for every hour of every day.
     - Trains a **Random Forest Regressor** model to predict the expected demand (quantity) given an hour, day, and dish.
   * **Output**: `canteen_model.pkl` (Trained Model) and `dish_encoder.pkl` (Label Encoder for dishes).

3. **Backend API**
   * **Script**: `app.py`
   * **Process**: Built with **FastAPI**, this backend loads the trained model artifacts. It exposes the `/api/predict` endpoint, which generates demand predictions for all dishes across all college hours (8 AM - 5 PM) for a given day. It then aggregates these predictions to identify the Top 3 Peak Hours and the Top 4 Dishes to prep.
   * **Output**: A RESTful JSON API.

4. **Frontend UI**
   * **File**: `frontend/index.html`
   * **Process**: A clean, responsive dashboard built with Vanilla HTML/CSS/JS. It fetches the daily predictions from the FastAPI backend and visually presents "Predicted Peak Hours" and a "Priority Prep List" for the canteen staff.

## Prerequisites

Ensure you have Python 3.8+ installed.

```bash
pip install -r requirements.txt
```

## Running the System

Follow these steps to run the complete system from scratch:

**Step 1: Generate Mock Data**
```bash
python generate_data.py
```
*This will create `datasets/canteen_pos_data.csv`.*

**Step 2: Train the ML Model**
```bash
python train_model.py
```
*This will analyze the data, train the model, and save `canteen_model.pkl` and `dish_encoder.pkl`.*

**Step 3: Start the Backend & Frontend**
```bash
uvicorn app:app --reload
```
*The FastAPI server will start, serving the API on `http://127.0.0.1:8000/api/predict` and the Frontend Dashboard on `http://127.0.0.1:8000/`.*

**Step 4: View the Dashboard**
Open your web browser and navigate to:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Tech Stack
* **Machine Learning:** Scikit-Learn, Pandas, NumPy
* **Backend API:** FastAPI, Uvicorn
* **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
