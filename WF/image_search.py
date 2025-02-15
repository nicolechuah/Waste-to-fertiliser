import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model
import shelve
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Load Teachable Machine model
MODEL_PATH = os.path.abspath('model/keras_model.h5')
LABELS_PATH = os.path.abspath('model/labels.txt')
model = load_model(MODEL_PATH)

# Load class labels
with open(LABELS_PATH, 'r') as f:
    labels = [line.strip().split(' ', 1)[1] for line in f.readlines()]

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))  # Resize to match model input
    img = np.expand_dims(img, axis=0) / 255.0  # Normalize
    return img

@app.route('/search-by-image', methods=['POST'])
def search_by_image():
    if 'image' not in request.files:
        return jsonify({'success': False, 'message': 'No image uploaded'})
    
    file = request.files['image']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    
    img = preprocess_image(filename)
    predictions = model.predict(img)
    predicted_label = labels[np.argmax(predictions)]
    
    # Search in the database
    db = shelve.open('storage.db')
    products_dict = db.get('Products', {})
    db.close()
    
    for product_id, product in products_dict.items():
        if predicted_label.lower() in product.get_name().lower():
            return jsonify({'success': True, 'product_id': product_id})
    
    return jsonify({'success': False, 'message': 'No matching product found'})

if __name__ == '__main__':
    app.run(debug=True)
