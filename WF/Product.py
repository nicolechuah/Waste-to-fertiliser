import shelve

class Product():
    product_id = 0
    
    def __init__(self, name, description, qty, selling_price, cost_price, visible, images,category):
        Product.product_id += 1
        self.__product_id = Product.product_id
        self.__name = name
        self.__description = description
        self.__qty = qty
        self.__selling_price = selling_price
        self.__cost_price = cost_price
        self.__visible = visible
        self.__images_id = images
        self.__category = category
    

    
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
    
    def get_category(self):
        return self.__category
    
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
        
    def set_category(self, category):
        self.__category = category
    
    def get_images_id(self):
        return self.__images_id 
            
    def get_all_images(self):
        all_images = []
        images_dict = {}
        try:
            db = shelve.open('storage.db')
            images_dict = db['Images']
        except:
            print('Error in retrieving images from storage.db')
        for image_id in self.__images_id:
            image = images_dict.get(image_id)
            all_images.append(image)
        return all_images
    
    def display_first_img(self):
        all_images = self.get_all_images()
        if len(all_images) > 0:
            return all_images[0]
        
    def add_image_id(self, image_id):
        self.__images_id.append(image_id)
        
    def get_images_with_id(self):
        image_and_id = []
        images = self.get_all_images()
        image_id = self.__images_id
        for i in range(len(images)):
            image_and_id.append((images[i], image_id[i]))
        return image_and_id
    
    def remove_image_id(self, image_id):
        self.__images_id.remove(image_id)
    
    def check_default_image(self):
        print(f"images id: {self.__images_id}")
        if len(self.__images_id) == 0:
            self.__images_id.append(1)
        if 1 in self.__images_id and len(self.__images_id) > 1:
            self.__images_id.remove(1)
        print(f"images id: {self.__images_id}")
            
    
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
        return f"Product ID: {self.__product_id}, Name: {self.__name}, Image: {self.__images_id}, Category: {self.__category}, Description: {self.__description}, Quantity: {self.__qty}, Selling Price: {self.__selling_price}, Cost Price: {self.__cost_price}, Visible: {self.__visible}"