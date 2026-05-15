from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import tensorflow as tf
# import keras
import numpy as np
from PIL import Image
import io

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
# keras.models.load_model("disease_detector_model.keras")
model = tf.keras.models.load_model(
    '../disease_detector_model.keras',
    compile=False
)

# Classes
class_names = [
    'Acne', 'Actinic_Keratosis', 'Benign_tumors', 'Bullous',
    'Candidiasis', 'DrugEruption', 'Eczema', 'Infestations_Bites',
    'Lichen', 'Lupus', 'Moles', 'Psoriasis', 'Rosacea',
    'Seborrh_Keratoses', 'SkinCancer', 'Sun_Sunlight_Damage',
    'Tinea', 'Unknown_Normal', 'Vascular_Tumors',
    'Vasculitis', 'Vitiligo', 'Warts'
]

# Home route
@app.get('/')
def homePage():
    return {'Message': 'Hello the API is working'}

# Prediction route
@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    # Read image bytes
    contents = await file.read()
    # Open image
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    # Resize to model input size
    image = image.resize((224, 224))
    # Convert to numpy
    image = np.array(image)
    # Normalize
    image = image / 255.0
    # Add batch dimension
    image = np.expand_dims(image, axis=0)
    # Prediction
    prediction = model.predict(image)
    predicted_index = np.argmax(prediction)
    predicted_class = class_names[predicted_index]
    confidence = float(np.max(prediction) * 100)
    return {
        'predicted': predicted_class,
        'confidence': round(confidence, 2)
    }