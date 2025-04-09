import os
import pickle
import numpy as np
from django.shortcuts import render, redirect
from django.conf import settings
from sklearn.preprocessing import LabelEncoder
from django.contrib.auth.decorators import login_required

# Load trained Random Forest model
model_path = os.path.join(settings.BASE_DIR, 'water_prediction', 'models', 'RandomForest_water_requirement1.pkl')
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# CROP LabelEncoder
crops = [
    "wheat", "rice", "maize", "sugarcane", "potato", "tomato", "cotton", "banana",
    "barley", "millet", "soybean", "peanut", "chickpea", "lentil", "onion", "garlic",
    "mustard", "groundnut"
]
le = LabelEncoder()
le.fit(crops)

# Crop Emojis
crop_emojis = {
    "wheat": "🌾", "rice": "🌾", "maize": "🌽", "sugarcane": "🍬", "potato": "🥔",
    "tomato": "🍅", "cotton": "🧵", "banana": "🍌", "barley": "🌿", "millet": "🌾",
    "soybean": "🫘", "peanut": "🥜", "chickpea": "🌱", "lentil": "🥬", "onion": "🧅",
    "garlic": "🧄", "mustard": "🌿", "groundnut": "🥜"
}

@login_required(login_url='login')
def water_prediction(request):
    if request.method == "POST":
        try:
            soil_moisture = float(request.POST["soil_moisture"])
            temperature = float(request.POST["temperature"])
            humidity = float(request.POST["humidity"])
            rainfall = float(request.POST["rainfall"])
            acre = float(request.POST["acre"])
            crop = request.POST["crop"].lower()

            # Encode the crop
            crop_encoded = le.transform([crop])[0]

            # Input data with 6 features including acre
            input_data = np.array([[soil_moisture, temperature, humidity, rainfall, acre, crop_encoded]])

            # Predict total water requirement
            prediction = model.predict(input_data)[0]

            # Emoji
            emoji = crop_emojis.get(crop, "🌱")

            # Save result in session for GET display
            request.session["prediction"] = round(prediction, 2)
            request.session["emoji"] = emoji
            request.session["acre"] = acre
            request.session["crop"] = crop

            return redirect("water_prediction")

        except Exception as e:
            request.session["error"] = "Invalid input. Please check your values."
            return redirect("water_prediction")

    # For GET requests
    prediction = request.session.pop("prediction", None)
    emoji = request.session.pop("emoji", None)
    acre = request.session.pop("acre", None)
    crop = request.session.pop("crop", None)
    error = request.session.pop("error", None)

    return render(request, "water_prediction.html", {
        "prediction": prediction,
        "emoji": emoji,
        "acre": acre,
        "crop": crop,
        "error": error,
        "crops": crops
    })
