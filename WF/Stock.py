import shelve
from datetime import datetime

class Stock:
    stock_id = 1
    def __init__(self, product_id, quantity, date = str(datetime.today().strftime('%Y-%m-%d'))):
        Stock.stock_id += 1
        self.__id = Stock.stock_id
        self.__product_id = product_id
        self.__quantity = quantity
        self.__product_name = None
        self.__date = date
        self.__confirmed = False
    
    def get_stock_id(self):
        return self.__id
    
    def get_product_id(self):
        return self.__product_id
    def set_product_id(self, product_id):
        self.__product_id = product_id
    
    def get_quantity(self):
        return self.__quantity
    def set_quantity(self, quantity):
        self.__quantity = quantity

    def get_product_name(self):
        db = shelve.open('storage.db')
        product = db['Products']
        db.close()
        
        for key in product:
            if product[key].get_product_id() == self.__product_id:
                
                self.__product_name = product.get(key).get_name()
                return self.__product_name
        return "Product not found"
    
    def get_date(self):
        return self.__date
    
    def set_date(self, date):
        self.__date = date
    
    def get_confirmed_status(self):
        return self.__confirmed
    
    def confirmed(self):
        self.__confirmed = True
    
    
        