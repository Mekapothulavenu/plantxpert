from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
import os
import pickle
import numpy as np
from django.conf import settings

# Load the ML model
model_path = os.path.join(settings.BASE_DIR, 'crop_recommendation', 'models', 'RandomForest.pkl')
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Crop Emojis Dictionary
crop_emojis = {
    "Rice": "🌾", "Maize": "🌽", "Chickpea": "🌱", "Kidney Beans": "🫘",
    "Pigeon Peas": "🌿", "Moth Beans": "🥜", "Mung Bean": "🌿",
    "Black Gram": "🌱", "Lentil": "🥬", "Pomegranate": "🍎",
    "Banana": "🍌", "Mango": "🥭", "Grapes": "🍇", "Watermelon": "🍉",
    "Muskmelon": "🍈", "Apple": "🍏", "Orange": "🍊", "Papaya": "🍈",
    "Coconut": "🥥", "Cotton": "🧵", "Jute": "🪢", "Coffee": "☕"
}

@login_required(login_url='login')
def crop_recommendation(request):
    if request.method == "POST":
        try:
            nitrogen = float(request.POST["nitrogen"])
            phosphorus = float(request.POST["phosphorus"])
            potassium = float(request.POST["potassium"])
            temperature = float(request.POST["temperature"])
            humidity = float(request.POST["humidity"])
            ph_level = float(request.POST["ph_level"])
            rainfall = float(request.POST["rainfall"])

            input_data = np.array([[nitrogen, phosphorus, potassium,
                                    temperature, humidity, ph_level, rainfall]])
            prediction = model.predict(input_data)[0]
            emoji = crop_emojis.get(prediction, "🌱")

            # Store in session and redirect
            request.session['prediction'] = prediction
            request.session['emoji'] = emoji
            return redirect(reverse('crop_recommendation'))

        except ValueError:
            request.session['error'] = "Invalid input values! Please enter numeric values."
            return redirect(reverse('crop_recommendation'))

    # Handle GET request
    prediction = request.session.pop('prediction', None)
    emoji = request.session.pop('emoji', None)
    error = request.session.pop('error', None)

    return render(request, "crop_recommendation.html", {
        "prediction": prediction,
        "emoji": emoji,
        "error": error
    })
