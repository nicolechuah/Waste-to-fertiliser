import os
import secrets
from flask import current_app as app


class Image:
    @staticmethod
    def save_image(image):
        random_hex = secrets.token_hex(8) #randomize filename
        f_name, f_ext = os.path.splitext(image.filename) #split filename and extension
        image_fn = random_hex + f_ext #combine random hex and extension
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_fn) #combine root path and image path
        image.save(image_path) #save image to path, save function is under the werkzeug library
        return image_fn
    
    @staticmethod
    def delete_image(image):
        print(image)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image)
        if os.path.exists(image_path) and image != "default_product.png":
            os.remove(image_path)
    
    def __str__(self):
        return f"Current Image ID {Image.Image_ID}"