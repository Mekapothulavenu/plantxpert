import os
import pickle
import numpy as np
from django.shortcuts import render, redirect
from django.conf import settings
from sklearn.preprocessing import LabelEncoder
from django.contrib.auth.decorators import login_required

# Load model & encoders
base_model_path = os.path.join(settings.BASE_DIR, 'fertilizers_prediction', 'models')

with open(os.path.join(base_model_path, 'decision_tree_fertilizer.pkl'), 'rb') as f:
    model = pickle.load(f)

with open(os.path.join(base_model_path, 'le_crop.pkl'), 'rb') as f:
    le_crop = pickle.load(f)

with open(os.path.join(base_model_path, 'le_soil.pkl'), 'rb') as f:
    le_soil = pickle.load(f)

with open(os.path.join(base_model_path, 'le_fert.pkl'), 'rb') as f:
    le_fert = pickle.load(f)

# Dropdown options
crop_types = le_crop.classes_
soil_types = le_soil.classes_

# Emoji map
crop_emojis = {
    "wheat": "🌾", "rice": "🌾", "maize": "🌽", "sugarcane": "🍬", "potato": "🥔",
    "tomato": "🍅", "cotton": "🧵", "banana": "🍌", "barley": "🌿", "millet": "🌾",
    "soybean": "🫘", "peanut": "🥜", "chickpea": "🌱", "lentil": "🥬", "onion": "🧅",
    "garlic": "🧄", "mustard": "🌿", "groundnut": "🥜"
}


@login_required(login_url='login')
def fertilizer_prediction(request):
    if request.method == "POST":
        try:
            crop = request.POST.get("crop")
            soil = request.POST.get("soil")
            nitrogen = float(request.POST.get("nitrogen"))
            phosphorus = float(request.POST.get("phosphorus"))
            potassium = float(request.POST.get("potassium"))
            temperature = float(request.POST.get("temperature"))
            humidity = float(request.POST.get("humidity"))
            acre = int(request.POST.get("acre"))

            crop_encoded = le_crop.transform([crop])[0]
            soil_encoded = le_soil.transform([soil])[0]

            features = np.array([[nitrogen, phosphorus, potassium, temperature,
                                  humidity, crop_encoded, soil_encoded, acre]])
            pred_encoded = model.predict(features)[0]
            predicted_fert = le_fert.inverse_transform([pred_encoded])[0]

            emoji = crop_emojis.get(crop.lower(), "🌱")

            request.session['predicted_fert'] = predicted_fert
            request.session['crop'] = crop
            request.session['soil'] = soil
            request.session['emoji'] = emoji

            return redirect("fertilizer_prediction")

        except Exception as e:
            print("Error:", e)
            request.session['error'] = "❌ Invalid input. Please check your values."
            return redirect("fertilizer_prediction")

    # GET
    return render(request, "fertilizer_prediction.html", {
        "prediction": request.session.pop("predicted_fert", None),
        "crop": request.session.pop("crop", None),
        "soil": request.session.pop("soil", None),
        "emoji": request.session.pop("emoji", None),
        "error": request.session.pop("error", None),
        "crop_types": crop_types,
        "soil_types": soil_types,
    })

