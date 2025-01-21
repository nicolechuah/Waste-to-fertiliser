class Review:
    review_id = 0
    def __init__(self, author, rating, comment, product_id):
        Review.review_id += 1
        self.__review_id = Review.review_id
        self.__author = author
        self.__rating = rating
        self.__comment = comment
        self.__product_id = product_id
        
    def get_review_id(self):
        return self.__review_id
    
    def get_author(self):
        return self.__author
    
    def get_rating(self):
        return self.__rating
    
    def get_comment(self):
        return self.__comment
    
    def get_product_id(self):
        return self.__product_id
    
    def set_rating(self, rating):
        self.__rating = rating
        
    def set_comment(self, comment):
        self.__comment = comment
    
    def set_author(self, author):
        self.__author = author
        
    def set_product_id(self, product_id):
        self.__product_id = product_id

    def __str__(self):
        return f"Author: {self.__author}, Rating: {self.__rating}, Comment: {self.__comment} Product ID: {self.__product_id}"