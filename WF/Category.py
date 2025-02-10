class Category:
    CategoryID = 3
    def __init__(self, name):
        if name == "Uncategorized":
            self.__category_id = 1
            self.__name = name
        else:
            Category.CategoryID += 1
            self.__category_id = Category.CategoryID
            self.__name = name 
            
            
    def get_category_id(self):
        return self.__category_id
    
    def get_name(self):
        return self.__name
    
    