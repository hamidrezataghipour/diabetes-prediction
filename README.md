# Diabetes Risk Prediction Web Application

This web application provides a user-friendly interface for predicting diabetes risk using a pre-trained TensorFlow model. Users can input their health information and receive an instant risk assessment.

## Features

- Clean, modern UI with responsive design
- Real-time form validation
- Visual risk meter
- Result display with probability percentage
- Backend powered by Flask and TensorFlow
- Medical disclaimer for AI-generated predictions
- Footer with copyright information and social links

## Project Structure

```
diabetes_model/
├── app.py                  # Flask API backend
├── diabetes_model_final.h5 # Pre-trained TensorFlow model
├── templates/
│   └── index.html          # Main HTML template
├── static/
│   ├── css/
│   │   └── styles.css      # CSS styles
│   ├── js/
│   │   └── script.js       # JavaScript for frontend logic
│   └── images/             # Images folder
│       ├── linkedin_icon.png  # LinkedIn icon
│       └── github_icon.png    # GitHub icon
└── README.md               # Project documentation
```

## Setup and Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package manager)

### Installation Steps

1. Clone this repository or download the source code.

2. Install the required dependencies:

   ```
   pip install flask tensorflow pandas scikit-learn numpy
   ```

3. Run the application:

   ```
   python app.py
   ```

4. Open your web browser and go to:
   ```
   http://127.0.0.1:5000
   ```

## Model Information

- The application uses a pre-trained TensorFlow model (`diabetes_model_final.h5`) for predictions.
- The model expects the following input features:
  - Numeric features:
    - `age`: Age in years (18-100)
    - `bmi`: Body Mass Index (10-50)
    - `HbA1c_level`: Hemoglobin A1c level (3.0-10.0)
    - `blood_glucose_level`: Blood glucose level (50-300)
    - `hypertension`: 0 (No) or 1 (Yes)
    - `heart_disease`: 0 (No) or 1 (Yes)
  - Categorical features:
    - `gender_Male`: 0 (Female) or 1 (Male)
    - `smoking_history`: One of 'current', 'ever', 'former', 'never', or 'not current'
- Prediction threshold: 0.07 (Returns "Diabetic" if probability > 0.07)

## Usage

1. Fill in all the required fields in the form.
2. Click the "Predict" button.
3. View your diabetes risk prediction and probability score.
4. Note the medical disclaimer below the prediction.

## New Features

### Medical Disclaimer

A disclaimer now appears after a prediction is made, reminding users that the AI-generated result is not a replacement for professional medical advice.

### Copyright and Social Links Footer

- A new footer at the bottom of the page displays copyright information.
- Links to the developer's LinkedIn and GitHub profiles are provided with hover effects.

## Footer Fix

- Pinned footer to bottom using flexbox and `min-height: 100vh`.
- Aligned copyright and icons horizontally with `flex: nowrap`.
- Prevented content overlap with `flex: 1 0 auto` on container.
- Added subtle yellow border top for separation and improved styling.
- Fixed responsive behavior for mobile view.

## UI Enhancement

- Applied glassmorphism effect to form and result boxes:
  - Semi-transparent background with blur effect for a frosted glass look
  - Subtle white borders and soft glow box-shadow
  - Improved readability with higher contrast text colors
- Updated the background with a diagonal gradient:
  - Used yellow (#FFC107), black (#1A1A1A), and white (#FFFFFF) colors
  - Added depth perception and visual interest to the interface
- Maintained color scheme consistency:
  - Yellow (#FFC107) for buttons and accents
  - Green (#28A745) for "Non-Diabetic" results
  - Red (#DC2626) for "Diabetic" results
- Enhanced form elements with semi-transparent backgrounds
- Improved visual hierarchy with proper spacing and typography
- Added text shadow to header for better readability against the gradient background

## UI Simplification

- Replaced glassmorphism effect with solid box design:
  - Changed to solid dark gray (#2D2D2D) background for form and result boxes
  - Added yellow (#FFC107) border for consistent branding
  - Applied subtle box-shadow (0 4px 8px rgba(0, 0, 0, 0.3)) for depth
  - Removed backdrop filters and transparency for improved performance
- Updated gradient background for a smoother experience:
  - Simplified to a two-color gradient (yellow to black)
  - Changed direction to top-to-bottom for a clean transition
  - Ensured consistent color theme across the application
- Maintained all existing functionality:
  - Form layout and validation
  - Result animations and styling
  - Yellow accent colors for buttons and interactive elements
  - Responsive design for various screen sizes
  - Sticky footer with social links

## Image Requirements

- `linkedin_icon.png`: LinkedIn logo (24x24px)
- `github_icon.png`: GitHub logo (24x24px)

## Notes

- This application is for educational purposes only and does not replace professional medical advice.
- The model's accuracy depends on the quality of the training data and may not be suitable for all populations.
- For optimal performance, ensure your browser is up-to-date.

## Troubleshooting

If you encounter any issues:

- Make sure all dependencies are installed correctly
- Check that the model file (`diabetes_model_final.h5`) is in the project's root directory
- Verify that port 5000 is not in use by another application
- Ensure the social media icon files exist in the images directory
