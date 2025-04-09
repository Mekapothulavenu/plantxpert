from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import os
import pickle
import numpy as np
import pandas as pd
from django.conf import settings

# Load Preprocessor
preprocessor_path = os.path.join(settings.BASE_DIR, 'yield_prediction', 'models', 'preprocesser.pkl')
with open(preprocessor_path, 'rb') as file:
    preprocessor = pickle.load(file)

# Load Model
model_path = os.path.join(settings.BASE_DIR, 'yield_prediction', 'models', 'RandomForestYieldPrediction.pkl')
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Load dataset for dropdown options
dataset_path = os.path.join(settings.BASE_DIR, 'yield_prediction', 'data', 'yield_df.csv')
df = pd.read_csv(dataset_path)

@login_required(login_url='login')
def crop_yield_prediction(request):
    areas = df['Area'].unique()
    items = df['Item'].unique()

    if request.method == "POST":
        try:
            # Get user input
            Year = int(request.POST.get("Year"))
            average_rainfall = float(request.POST.get("average_rainfall"))
            pesticides_tonnes = float(request.POST.get("pesticides_tonnes"))
            avg_temp = float(request.POST.get("avg_temp"))
            Area = request.POST.get("Area")
            Item = request.POST.get("Item")

            # Prepare and preprocess input data
            input_data = np.array([[Year, average_rainfall, pesticides_tonnes, avg_temp, Area, Item]], dtype=object)
            transformed_data = preprocessor.transform(input_data)

            # Predict yield
            predicted_yield = model.predict(transformed_data)[0]

            # Store prediction in session to avoid resubmission issues
            request.session['predicted_yield'] = round(predicted_yield, 2)

            # Redirect to clear POST data
            return redirect("crop_yield_prediction")

        except Exception as e:
            request.session['error'] = str(e)
            return redirect("crop_yield_prediction")

    # Retrieve results from session and clear session variables
    predicted_yield = request.session.pop('predicted_yield', None)
    error = request.session.pop('error', None)

    return render(request, "crop_yield_prediction.html", {
        "areas": areas,
        "items": items,
        "predicted_yield": predicted_yield,
        "error": error
    })

