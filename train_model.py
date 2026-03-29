import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

def train_and_save_model():
    print("Loading data...")
    df = pd.read_csv('datasets/canteen_pos_data.csv')
    
    # Feature Engineering
    # Convert Date and Time to datetime
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df['Hour'] = df['Datetime'].dt.hour
    df['DayOfWeek'] = df['Datetime'].dt.dayofweek
    
    # Aggregate data by Date, Hour, and Dish to get total quantity per hour
    agg_df = df.groupby(['Date', 'Hour', 'DayOfWeek', 'Dish'])['Quantity'].sum().reset_index()
    
    # Encode 'Dish'
    le = LabelEncoder()
    agg_df['Dish_Encoded'] = le.fit_transform(agg_df['Dish'])
    
    # Prepare features and target
    X = agg_df[['Hour', 'DayOfWeek', 'Dish_Encoded']]
    y = agg_df['Quantity']
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Model
    print("Training model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train.values, y_train.values) # using .values to avoid feature names warning later
    
    # Evaluate Model
    score = model.score(X_test.values, y_test.values)
    print(f"Model R^2 Score: {score:.4f}")
    
    # Save Model and Encoder
    print("Saving model and encoders...")
    joblib.dump(model, 'canteen_model.pkl')
    joblib.dump(le, 'dish_encoder.pkl')
    print("Done!")

if __name__ == "__main__":
    train_and_save_model()