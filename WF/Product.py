class Product():
    product_id = 0
    
    def __init__(self, name, description, qty, selling_price, cost_price, visible, image = "default_product.png"):
        Product.product_id += 1
        self.__product_id = Product.product_id
        self.__name = name
        self.__description = description
        self.__qty = qty
        self.__selling_price = selling_price
        self.__cost_price = cost_price
        self.__visible = visible
        self.__image = image

    
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
    
    def get_image(self):
        return self.__image
    
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
        
    def set_image(self, image):
        self.__image = image

        
    def __str__(self):
        return f"Product ID: {self.__product_id}, Name: {self.__name}, Image: {self.__image}, Qty:{self.__qty}"