import os
import numpy as np
import tensorflow as tf
import shelve
from flask import request, render_template
from PIL import Image, ImageOps
from fuzzywuzzy import fuzz

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model")
LABELS_PATH = os.path.join(os.path.dirname(__file__), "model", "labels.txt")

try:
    model = tf.saved_model.load(MODEL_PATH)
    infer = model.signatures["serving_default"]
    print(f"✅ Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None  

# Load class labels
with open(LABELS_PATH, "r") as f:
    labels = [line.strip().split(' ', 1)[1] for line in f.readlines()]  

np.set_printoptions(suppress=True)

def preprocess_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    return np.expand_dims(normalized_image_array, axis=0)

def search_by_image():
    """Handles image uploads and filters products based on name similarity."""
    UPLOAD_FOLDER = "static/images"

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if 'image' not in request.files:
        db = shelve.open('storage.db')
        products_dict = db.get('Products', {})
        db.close()
        return render_template('includes/home_partial.html', products_list=products_dict.values())

    file = request.files['image']
    filename = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filename)

    if model is None:
        return render_template('includes/home_partial.html', products_list=[])

    image_data = preprocess_image(filename)
    input_tensor = tf.convert_to_tensor(image_data, dtype=tf.float32)
    prediction = infer(tf.constant(input_tensor))

    prediction_values = list(prediction.values())[0].numpy()
    index = np.argmax(prediction_values)  
    predicted_label = labels[index].strip().lower()

    print(f"🔍 DEBUG: Predicted Label - '{predicted_label}'")  # Debugging line

    db = shelve.open('storage.db')
    products_dict = db.get('Products', {})
    db.close()

    ### ✅ **Improved Matching Logic**
    matching_products = []
    for product in products_dict.values():
        product_name = product.get_name().strip().lower()

        # **More accurate fuzzy matching** (ensures stronger matches)
        similarity_score = fuzz.token_set_ratio(predicted_label, product_name)

        # **Stricter threshold for multi-word matches**
        if similarity_score > 75:  # Adjust if needed
            matching_products.append(product)

        # **Double-word Check: Ensures BOTH words in predicted label exist in product name**
        elif all(word in product_name for word in predicted_label.split()):
            matching_products.append(product)

    # If nothing is found, return ALL products (like no search case)
    if not matching_products:
        matching_products = products_dict.values()

    return render_template('includes/home_partial.html', products_list=matching_products)

