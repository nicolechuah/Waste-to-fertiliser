import shelve

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
        if images == []:
            self.__images_id = [1] # default image ID
        else:
            self.__images_id = images # a list object of IDs

    

    
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
        
    def get_images_id(self):
        return self.__images_id #returns a list of ID of the images
    
    def add_image_id(self, image_id):
        self.__images_id.append(image_id) # make sure to only append the ID
        
    def remove_image_id(self, image_id):
        self.__images_id.remove(image_id) # make sure to only remove the ID
    
    def get_images(self):
        with shelve.open('storage.db') as db:
            image_db = db['Images']
            images = []
            for image_id in self.__images_id:
                if image_id in image_db:
                    image = image_db[image_id]  # get the image object from the ID
                    images.append(image.get_image())  # get the image name from the object
                else:
                    print(f"Image ID {image_id} not found in the database.")
        return images
    
    def get_images_with_id(self):
        with shelve.open('storage.db') as db:
            image_db = db['Images']
            images_with_id = []
            for image_id in self.__images_id:
                if image_id in image_db:
                    image = image_db[image_id]
                    images_with_id.append((image.get_image(), image_id))
                else:
                    print(f"Image ID {image_id} not found in the database.")
        return images_with_id

    def delete_all_images(self): #use only when deleting a product object
        with shelve.open('storage.db') as db:
            image_db = db['Images']
            for image_id in self.__images_id:
                if image_id in image_db:
                    image = image_db[image_id]  # retrieve that image object
                    image.delete_image(image.get_image())
                    del image_db[image_id]
            db['Images'] = image_db
            
    def add_default_image(self):
        if len(self.__images_id) == 0:
            self.__images_id.append(1)
    
    def remove_default_image(self):
        if 1 in self.__images_id and len(self.__images_id) > 1:
            self.__images_id.remove(1)
    
    
    def get_average_rating(self):
        try:
            storage = shelve.open('storage.db')
            reviews = storage['Reviews']
            total = 0
            count = 0
            related_reviews = []
            for reviewID, object in reviews.items(): # only retrieving the ID of the reviews
                
                if object.get_product_id() == self.get_product_id():
                    individual_rating = object.get_rating()
                    total +=  int(individual_rating)
                    count += 1
            if count == 0:
                return 0
            return f"{total/count:.2f}"
        except KeyError:
            storage['Reviews'] = {}
            return 0
            
    
            

            
    def __str__(self):
        return f"Product ID: {self.__product_id}, Name: {self.__name}, Image: {self.__images_id}, Qty:{self.__qty}"