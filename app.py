import os
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify, render_template
from sklearn.preprocessing import StandardScaler
import pandas as pd
import pickle

app = Flask(__name__)

# Load the model
model_path = 'diabetes_model_final.h5'
model = tf.keras.models.load_model(model_path)

# Define feature names in the correct order
numeric_features = ['age', 'bmi', 'HbA1c_level', 'blood_glucose_level', 'hypertension', 'heart_disease']
categorical_features = [
    'gender_Male', 
    'smoking_history_current', 
    'smoking_history_ever', 
    'smoking_history_former', 
    'smoking_history_never', 
    'smoking_history_not current',
    'smoking_history_No Info'  # Added missing feature
]

# Try to load scaler from pickle file, or create and save a new one if it doesn't exist
scaler_path = 'scaler.pkl'
if os.path.exists(scaler_path):
    try:
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        print("Loaded scaler from scaler.pkl")
    except Exception as e:
        print(f"Error loading scaler: {str(e)}")
        raise
else:
    # Create a scaler for numeric features
    # This is a simplified approach - in production, use the actual training data statistics
    print("Creating new scaler and saving to scaler.pkl")
    scaler = StandardScaler()
    sample_data = pd.DataFrame({
        'age': [20, 40, 60, 80],
        'bmi': [18, 25, 30, 40],
        'HbA1c_level': [4.0, 5.5, 7.0, 9.0],
        'blood_glucose_level': [80, 120, 180, 250],
        'hypertension': [0, 1, 0, 1],
        'heart_disease': [0, 0, 1, 1]
    })
    scaler.fit(sample_data)
    
    # Save the scaler for future use
    with open(scaler_path, 'wb') as f:
        pickle.dump(scaler, f)

@app.route('/')
def home():
    """Serve the home page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        # Get data from request
        data = request.get_json()
        print("Received data:", data)  # Debug information
        
        # Validate input data for required fields (exclude the new feature as it will be defaulted if missing)
        required_fields = numeric_features + [f for f in categorical_features if f != 'smoking_history_No Info']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create a DataFrame with all features (both numeric and categorical)
        input_data = {}
        
        # Extract numeric features
        for feature in numeric_features:
            value = float(data[feature])
            # Basic validation
            if feature == 'age' and (value < 0 or value > 120):
                return jsonify({'error': 'Age must be between 0 and 120'}), 400
            if feature == 'bmi' and (value < 10 or value > 60):
                return jsonify({'error': 'BMI must be between 10 and 60'}), 400
            if feature == 'HbA1c_level' and (value < 3.0 or value > 15.0):
                return jsonify({'error': 'HbA1c level must be between 3.0 and 15.0'}), 400
            if feature == 'blood_glucose_level' and (value < 50 or value > 500):
                return jsonify({'error': 'Blood glucose level must be between 50 and 500'}), 400
            if feature in ['hypertension', 'heart_disease'] and value not in [0, 1]:
                return jsonify({'error': f'{feature} must be 0 or 1'}), 400
            input_data[feature] = value
        
        # Extract categorical features (handle missing 'smoking_history_No Info' with default 0)
        for feature in categorical_features:
            if feature == 'smoking_history_No Info':
                # Default to 0 if not provided
                value = int(data.get(feature, 0))
            else:
                value = int(data[feature])
                
            if value not in [0, 1]:
                return jsonify({'error': f'{feature} must be 0 or 1'}), 400
            input_data[feature] = value
        
        # Create a DataFrame with the exact same format as what the model expects
        input_df = pd.DataFrame([input_data])
        print("Input DataFrame before scaling:", input_df)  # Debug information
        
        # Scale only the numeric features
        input_df[numeric_features] = scaler.transform(input_df[numeric_features])
        print("Input DataFrame after scaling:", input_df)  # Debug information
        
        # Convert DataFrame to array for model prediction
        features_array = input_df.values
        
        # Print the shape of the features array to ensure it's correct (should be (1, 13))
        print("Features array shape:", features_array.shape)  # Debug information
        
        # Make prediction
        prediction = model.predict(features_array)[0][0]
        
        # Apply threshold (0.07 as specified)
        result = "Diabetic" if prediction > 0.07 else "Non-Diabetic"
        
        # Return prediction
        return jsonify({
            'prediction': result,
            'probability': float(prediction)
        })
        
    except Exception as e:
        print("Error during prediction:", str(e))  # Debug information
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 