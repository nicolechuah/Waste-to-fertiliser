import os
import secrets
from flask import current_app as app

class Image:
    Image_ID = 2
    def __init__(self, image): #image name is still the file name
        Image.Image_ID += 1
        self.__image_id = Image.Image_ID
        self.__image = image #make sure to run save_image function first before creating an object
        
    def get_image_id(self):
        return self.__image_id
    
    def get_image(self):
        return self.__image
    
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
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image)
        if os.path.exists(image_path) and image != "default_product.png":
            os.remove(image_path)
    
    def __str__(self):
        return f"Image ID: {self.__image_id}\nImage: {self.__image}"