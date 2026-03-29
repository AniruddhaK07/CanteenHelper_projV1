import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_mock_data(days=60):
    dishes = ['Burger', 'Pizza', 'Pasta', 'Sandwich', 'Coffee', 'Tea', 'Fries', 'Salad']
    data = []
    
    start_date = datetime.now() - timedelta(days=days)
    
    for day in range(days):
        current_date = start_date + timedelta(days=day)
        # Skip Sundays
        if current_date.weekday() == 6:
            continue
            
        # College hours: 8 AM to 6 PM (18:00)
        for hour in range(8, 18):
            # Base number of orders
            num_orders = random.randint(5, 20)
            
            # Peak hours: 12 PM - 2 PM (Lunch), 4 PM - 5 PM (Snack)
            if 12 <= hour <= 13:
                num_orders += random.randint(30, 50)
            elif 15 <= hour <= 16:
                num_orders += random.randint(20, 35)
                
            for _ in range(num_orders):
                # Probabilities change based on time
                if 8 <= hour <= 10:
                    # Morning: Coffee, Tea, Sandwich
                    probs = [0.05, 0.05, 0.05, 0.3, 0.3, 0.2, 0.02, 0.03]
                elif 12 <= hour <= 14:
                    # Lunch: Burger, Pizza, Pasta, Salad
                    probs = [0.2, 0.2, 0.2, 0.1, 0.05, 0.05, 0.1, 0.1]
                elif 15 <= hour <= 17:
                    # Snack: Fries, Coffee, Tea, Sandwich
                    probs = [0.1, 0.1, 0.05, 0.2, 0.15, 0.15, 0.2, 0.05]
                else:
                    # Generic
                    probs = [0.125] * 8
                
                dish = np.random.choice(dishes, p=probs)
                quantity = random.randint(1, 3)
                
                # Randomize minutes and seconds
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                order_time = current_date.replace(hour=hour, minute=minute, second=second)
                
                data.append({
                    'Date': order_time.strftime('%Y-%m-%d'),
                    'Time': order_time.strftime('%H:%M:%S'),
                    'Dish': dish,
                    'Quantity': quantity
                })
                
    df = pd.DataFrame(data)
    df.to_csv('datasets/canteen_pos_data.csv', index=False)
    print(f"Generated {len(df)} records and saved to 'datasets/canteen_pos_data.csv'.")

if __name__ == "__main__":
    generate_mock_data()