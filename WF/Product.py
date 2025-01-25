from Image import Image

class Product():
    product_id = 0
    
    def __init__(self, name, description, qty, selling_price, cost_price, visible, images):
        Product.product_id += 1
        self.__product_id = Product.product_id
        self.__name = name
        self.__description = description
        self.__qty = qty
        self.__selling_price = selling_price
        self.__cost_price = cost_price
        self.__visible = visible
        self.__images = images
    

    
    def get_product_id(self):
        return self.__product_id
    
    def get_name(self):
        return self.__name
    
    def get_description(self):
        return self.__description
    
    def get_qty(self):
        return self.__qty
    
    def get_selling_price(self):
        return self.__selling_price
    
    def get_cost_price(self):
        return self.__cost_price
    
    def get_visible(self):
        return self.__visible
    
    def set_name(self, name):
        self.__name = name
        
    def set_description(self, description):
        self.__description = description
        
    def set_qty(self, qty):
        self.__qty = qty
        
    def set_selling_price(self, selling_price):
        self.__selling_price = selling_price
    
    def set_cost_price(self, cost_price):
        self.__cost_price = cost_price
    
    def set_visible(self, visible):
        self.__visible = visible
        
    def get_images(self):
        return self.__images #returns a list of ID of the images
    
    def add_image(self, image_id):
        self.__images.append(image_id) # make sure to only append the ID

        
    def __str__(self):
        return f"Product ID: {self.__product_id}, Name: {self.__name}, Image: {self.__images}, Qty:{self.__qty}"