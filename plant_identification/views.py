from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.decorators import login_required
import numpy as np
from PIL import Image
import os
import json
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load model
model_path = os.path.join(settings.BASE_DIR, 'Plant_identification', 'models', 'roboflow_plant_identification_model.h5')
model = load_model(model_path)

# Class index mapping
class_indices_path = os.path.join(settings.BASE_DIR, 'Plant_identification', 'data', 'class_names.json')
with open(class_indices_path, 'r') as f:
    class_indices = json.load(f)
index_to_class = {v: k for k, v in class_indices.items()}

# Plant info
json_path = os.path.join(settings.BASE_DIR, 'Plant_identification', 'data', 'plant_identification_details.json')
with open(json_path, 'r') as file:
    plant_data = json.load(file)
    plant_classes = [key.replace("___", " → ").replace("_", " ") for key in plant_data.keys()]

def clear_keras_session():
    tf.keras.backend.clear_session()

@login_required(login_url='login')
def plant_identification(request):
    if request.method == 'POST' and request.FILES.get('plant_image'):
        clear_keras_session()

        # Save uploaded image
        image_file = request.FILES['plant_image']
        file_path = default_storage.save('uploads/' + image_file.name, ContentFile(image_file.read()))
        image_url = settings.MEDIA_URL + file_path

        # Preprocess image
        img = Image.open(image_file).resize((224, 224)).convert("RGB")
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Predict
        prediction = model.predict(img_array)[0]
        predicted_index = np.argmax(prediction)
        predicted_class = index_to_class[predicted_index]
        confidence = float(prediction[predicted_index]) * 100
        result = predicted_class.replace('__', ' → ')

        # Plant info
        info = plant_data.get(predicted_class)
        if not info:
            info = {
                "description": "No information available.",
                "uses": "Not available.",
                "organic_benefits": "Not available.",
                "chemical_content": "Not available.",
                "precautions": "Not available."
            }
        info["plant"] = result

        # Store in session
        request.session['result'] = result
        request.session['confidence'] = confidence
        request.session['image_url'] = image_url
        request.session['details'] = info

        return redirect('plant_identification')  # Redirect to avoid POST warning

    # Load from session after redirect
    result = request.session.pop('result', None)
    confidence = request.session.pop('confidence', None)
    image_url = request.session.pop('image_url', None)
    info = request.session.pop('details', None)

    return render(request, 'plant_identification.html', {
        'result': result,
        'confidence': confidence,
        'image_url': image_url,
        'details': info,
        'plant_classes': plant_classes
    })
