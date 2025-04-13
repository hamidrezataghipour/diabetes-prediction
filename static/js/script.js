// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const form = document.getElementById('prediction-form');
    const loadingElement = document.getElementById('loading');
    const initialMessage = document.getElementById('initial-message');
    const predictionResult = document.getElementById('prediction-result');
    const predictionText = document.getElementById('prediction-text');
    const probabilityText = document.getElementById('probability-text');
    const riskIndicator = document.getElementById('risk-indicator');
    const smokingHistorySelect = document.getElementById('smoking_history');
    const disclaimerText = document.getElementById('disclaimer-text');
    const resetButton = document.getElementById('reset-button');
    
    // Add event listener for form submission
    form.addEventListener('submit', async function(event) {
        // Prevent default form submission
        event.preventDefault();
        
        // Validate form inputs
        if (!validateForm()) {
            return;
        }
        
        // Show loading spinner, hide initial message and any previous results
        loadingElement.classList.remove('hidden');
        initialMessage.classList.add('hidden');
        predictionResult.classList.add('hidden');
        
        // Hide disclaimer while loading
        if (disclaimerText) {
            disclaimerText.classList.add('hidden');
        }
        
        try {
            // Get form data
            const formData = getFormData();
            
            // Send data to API
            const prediction = await sendPredictionRequest(formData);
            
            // Process and display the result
            displayPredictionResult(prediction);
            
            // Show the disclaimer text after prediction
            if (disclaimerText) {
                disclaimerText.classList.remove('hidden');
            }
        } catch (error) {
            // Handle errors
            console.error('Error during prediction:', error);
            alert('An error occurred while processing your request. Please try again.');
        } finally {
            // Hide loading spinner
            loadingElement.classList.add('hidden');
        }
    });
    
    // Add event listener for reset button
    resetButton.addEventListener('click', function() {
        // Reset the form
        form.reset();
        
        // Hide results and show initial message
        predictionResult.classList.add('hidden');
        initialMessage.classList.remove('hidden');
        
        // Hide disclaimer
        if (disclaimerText) {
            disclaimerText.classList.add('hidden');
        }
        
        // Reset risk indicator
        riskIndicator.style.width = '0%';
    });
    
    // Function to validate form inputs
    function validateForm() {
        // Get all input values
        const age = parseFloat(document.getElementById('age').value);
        const bmi = parseFloat(document.getElementById('bmi').value);
        const hbA1c = parseFloat(document.getElementById('HbA1c_level').value);
        const bloodGlucose = parseFloat(document.getElementById('blood_glucose_level').value);
        
        // Validation checks
        if (age < 18 || age > 100) {
            alert('Age must be between 18 and 100.');
            return false;
        }
        
        if (bmi < 10 || bmi > 50) {
            alert('BMI must be between 10 and 50.');
            return false;
        }
        
        if (hbA1c < 3.0 || hbA1c > 10.0) {
            alert('HbA1c level must be between 3.0 and 10.0.');
            return false;
        }
        
        if (bloodGlucose < 50 || bloodGlucose > 300) {
            alert('Blood glucose level must be between 50 and 300.');
            return false;
        }
        
        return true;
    }
    
    // Function to get form data and format it for the API
    function getFormData() {
        // Get values from form inputs
        const age = parseFloat(document.getElementById('age').value);
        const bmi = parseFloat(document.getElementById('bmi').value);
        const hbA1c = parseFloat(document.getElementById('HbA1c_level').value);
        const bloodGlucose = parseFloat(document.getElementById('blood_glucose_level').value);
        const hypertension = parseInt(document.getElementById('hypertension').value);
        const heartDisease = parseInt(document.getElementById('heart_disease').value);
        const gender = parseInt(document.getElementById('gender').value);
        const smokingHistory = document.getElementById('smoking_history').value;
        
        // Create smoking history object with all options set to 0
        const smokingHistoryData = {
            'smoking_history_current': 0,
            'smoking_history_ever': 0,
            'smoking_history_former': 0,
            'smoking_history_never': 0,
            'smoking_history_not current': 0,
            'smoking_history_No Info': 0  // Add the missing feature, default to 0
        };
        
        // Set the selected smoking history option to 1
        if (smokingHistory === 'current') {
            smokingHistoryData['smoking_history_current'] = 1;
        } else if (smokingHistory === 'ever') {
            smokingHistoryData['smoking_history_ever'] = 1;
        } else if (smokingHistory === 'former') {
            smokingHistoryData['smoking_history_former'] = 1;
        } else if (smokingHistory === 'never') {
            smokingHistoryData['smoking_history_never'] = 1;
        } else if (smokingHistory === 'not_current') {
            smokingHistoryData['smoking_history_not current'] = 1;
        } else if (smokingHistory === 'no_info') {
            smokingHistoryData['smoking_history_No Info'] = 1;
        }
        
        // Combine all data
        return {
            'age': age,
            'bmi': bmi,
            'HbA1c_level': hbA1c,
            'blood_glucose_level': bloodGlucose,
            'hypertension': hypertension,
            'heart_disease': heartDisease,
            'gender_Male': gender,
            ...smokingHistoryData
        };
    }
    
    // Function to send prediction request to API
    async function sendPredictionRequest(data) {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Server error');
        }
        
        return response.json();
    }
    
    // Function to display prediction result
    function displayPredictionResult(prediction) {
        // Show prediction result container
        predictionResult.classList.remove('hidden');
        
        // Update prediction text
        predictionText.textContent = prediction.prediction;
        
        // Set appropriate class based on prediction
        if (prediction.prediction === 'Diabetic') {
            predictionText.className = 'positive';
        } else {
            predictionText.className = 'negative';
        }
        
        // Update probability text
        const probabilityPercentage = (prediction.probability * 100).toFixed(1);
        probabilityText.textContent = `Risk Probability: ${probabilityPercentage}%`;
        
        // Update risk indicator position
        riskIndicator.style.width = `${prediction.probability * 100}%`;
    }
}); 