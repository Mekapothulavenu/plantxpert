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

# Load model and class indices
model_path = os.path.join(settings.BASE_DIR, 'Pest_prediction', 'models', 'roboflow_pest_identification_model5.h5')
pest_model = load_model(model_path)

class_indices_path = os.path.join(settings.BASE_DIR, 'Pest_prediction', 'data', 'pest_class_indices.json')
with open(class_indices_path, 'r') as f:
    pest_class_indices = json.load(f)
index_to_class = {v: k for k, v in pest_class_indices.items()}

solution_path = os.path.join(settings.BASE_DIR, 'Pest_prediction', 'data', 'pest_solutions.json')
with open(solution_path, 'r') as f:
    pest_solutions = json.load(f)
    pest_classes = [key.replace("___", " → ").replace("_", " ") for key in pest_solutions.keys()]

def clear_keras_session():
    tf.keras.backend.clear_session()

@login_required(login_url='login')
def pest_prediction(request):
    if request.method == 'POST' and request.FILES.get('pest_image'):
        clear_keras_session()
        image_file = request.FILES['pest_image']
        file_path = default_storage.save('uploads/' + image_file.name, ContentFile(image_file.read()))
        image_url = settings.MEDIA_URL + file_path

        img = Image.open(image_file).resize((224, 224)).convert("RGB")
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = pest_model.predict(img_array)[0]
        predicted_index = np.argmax(prediction)
        predicted_class = index_to_class[predicted_index]
        confidence = float(prediction[predicted_index]) * 100
        readable_result = predicted_class.replace('__', ' → ')

        solution = pest_solutions.get(predicted_class, {
            "description": "No information available.",
            "cure": "Not Available",
            "organic_solution": "Not Available",
            "chemical_solution": "Not Available",
            "preventive_measures": "Not Available"
        })
        solution["pest"] = readable_result

        request.session['pest_result'] = readable_result
        request.session['pest_confidence'] = confidence
        request.session['pest_image_url'] = image_url
        request.session['pest_solution'] = solution

        return redirect('pest_prediction')

    result = request.session.pop('pest_result', None)
    confidence = request.session.pop('pest_confidence', None)
    image_url = request.session.pop('pest_image_url', None)
    solution = request.session.pop('pest_solution', None)

    return render(request, 'pest_prediction.html', {
        'result': result,
        'confidence': confidence,
        'image_url': image_url,
        'solution': solution,
        'pest_classes': pest_classes
    })
