#!/usr/bin/env python
"""
Script to create and save a StandardScaler for the diabetes prediction model.
This ensures that the scaler is properly fitted with feature names and can
be loaded by the main application.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle
import os

def create_and_save_scaler(output_path='scaler.pkl'):
    """
    Create a StandardScaler fitted with a sample dataset with appropriate
    feature names, and save it to a pickle file.
    
    Args:
        output_path: Path where the pickle file will be saved
    """
    print(f"Creating scaler and saving to {output_path}")
    
    # Define numeric features (these must match the ones used in app.py)
    numeric_features = [
        'age', 'bmi', 'HbA1c_level', 'blood_glucose_level', 
        'hypertension', 'heart_disease'
    ]
    
    # Create sample data with reasonable ranges
    sample_data = pd.DataFrame({
        'age': [20, 40, 60, 80],
        'bmi': [18, 25, 30, 40],
        'HbA1c_level': [4.0, 5.5, 7.0, 9.0],
        'blood_glucose_level': [80, 120, 180, 250],
        'hypertension': [0, 1, 0, 1],
        'heart_disease': [0, 0, 1, 1]
    })
    
    # Create and fit the scaler
    scaler = StandardScaler()
    scaler.fit(sample_data)
    
    # Save the scaler to disk
    with open(output_path, 'wb') as f:
        pickle.dump(scaler, f)
    
    print(f"Scaler successfully saved to {output_path}")
    print(f"Feature names used: {sample_data.columns.tolist()}")
    print(f"Mean values: {scaler.mean_}")
    print(f"Scale values: {scaler.scale_}")

if __name__ == "__main__":
    # Check if scaler already exists
    if os.path.exists('scaler.pkl'):
        overwrite = input("scaler.pkl already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Operation cancelled.")
            exit(0)
    
    # Create and save the scaler
    create_and_save_scaler()
    print("Done. You can now run the Flask application (app.py).") 