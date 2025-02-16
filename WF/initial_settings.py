from Product import Product
from Stock import Stock
from User import User
from Review import Review
import shelve

product_list = [Product("Organic Fertiliser - 100g", "This organic fertiliser is made from our food waste compost. It contains no chemical, contains no harmful pathogens, improves soil organic matter, serves as a strong foundation to bare soil, is suitable for all plants, creates savings for users,has a high NPK value and no offensive odour.",500,3.00, 0.50, True,[1],["All", "Fertiliser"]), 
 Product("Sunflower seeds", "These sunflower seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 50-60 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Vegetable Seeds", "These vegetable seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 30-40 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Gloves", "These garden gloves are made of durable rubber and are suitable for gardening. They have a grip on the palm and are easy to clean.",50,10.00, 2.00, True,[1],["All", "Tools"]), 
 Product("Herb Seeds", "These herb seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 20-30 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Rake", "This garden rake is made of durable metal and is suitable for gardening. It has a sturdy handle and is easy to clean.",50,15.00, 3.00, True,[1],["All", "Tools"]), 
 Product("Organic Fertiliser - 200g", "This organic fertiliser is made from our food waste compost. It contains no chemical, contains no harmful pathogens, improves soil organic matter, serves as a strong foundation to bare soil, is suitable for all plants, creates savings for users,has a high NPK value and no offensive odour.",500,3.50, 0.60, True,[1],["All", "Fertiliser"]), 
 Product("Tomato Seeds", "These tomato seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 60-90 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Fork", "This garden fork is made of durable metal and is suitable for gardening. It has a sturdy handle and is easy to clean.",50,15.00, 3.00, True,[1],["All", "Tools"]), 
 Product("Compost Tea Fertiliser", "This compost tea fertiliser is made from compost tea and is suitable for all plants. It has a high NPK value and is easy to use.",50,10.00, 2.00, True,[1],["All", "Fertiliser"]), 
 Product("Cucumber Seeds", "These cucumber seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 50-60 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Organic Fertiliser - 500g", "This organic fertiliser is made from our food waste compost. It contains no chemical, contains no harmful pathogens, improves soil organic matter, serves as a strong foundation to bare soil, is suitable for all plants, creates savings for users,has a high NPK value and no offensive odour.",500,4.00, 0.80, True,[1],["All", "Fertiliser"]), 
 Product("Carrot Seeds", "These carrot seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 60-90 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Pruning Shears", "These garden pruning shears are made of durable metal and are suitable for pruning plants. They have a sharp blade and are easy to clean.",50,20.00, 4.00, True,[1],["All", "Tools"]), 
 Product("Fertiliser Injector", "This fertiliser injector is made of durable plastic and is suitable for injecting fertiliser into soil. It has a capacity of 20 litres and is easy to assemble.",50,25.00, 6.00, True,[1],["All", "Tools"]), 
 Product("Pepper Seeds", "These pepper seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 60-90 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Rake with Handle", "This garden rake with handle is made of durable metal and is suitable for gardening. It has a sturdy handle and is easy to clean.",50,20.00, 4.00, True,[1],["All", "Tools"]), 
 Product("Organic Fertiliser - 1kg", "This organic fertiliser is made from our food waste compost. It contains no chemical, contains no harmful pathogens, improves soil organic matter, serves as a strong foundation to bare soil, is suitable for all plants, creates savings for users,has a high NPK value and no offensive odour.",500,5.00, 1.00, True,[1],["All", "Fertiliser"]), 
 Product("Cabbage Seeds", "These cabbage seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 60-90 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Trowel", "This garden trowel is made of durable metal and is suitable for gardening. It has a sturdy handle and is easy to clean.",50,15.00, 3.00, True,[1],["All", "Tools"]), 
 Product("Spinach Seeds", "These spinach seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 20-30 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Pruning Saw", "This garden pruning saw is made of durable metal and is suitable for pruning plants. It has a sharp blade and is easy to clean.",50,25.00, 5.00, True,[1],["All", "Tools"]), 
 Product("Fertiliser Injector with Handle", "This fertiliser injector with handle is made of durable plastic and is suitable for injecting fertiliser into soil. It has a capacity of 20 litres and is easy to assemble.",50,35.00, 8.00, True,[1],["All", "Tools"]), 
 Product("Broccoli Seeds", "These broccoli seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 60-90 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Rake with Wheels", "This garden rake with wheels is made of durable metal and is suitable for gardening. It has a sturdy handle and is easy to clean.",50,25.00, 5.00, True,[1],["All", "Tools"]), 
 Product("Organic Fertiliser - 2kg", "This organic fertiliser is made from our food waste compost. It contains no chemical, contains no harmful pathogens, improves soil organic matter, serves as a strong foundation to bare soil, is suitable for all plants, creates savings for users,has a high NPK value and no offensive odour.",500,6.00, 1.20, True,[1],["All", "Fertiliser"]), 
 Product("Kale Seeds", "These kale seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 60-90 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]),
 Product("Ceramic Pot - 8 inch", "This durable ceramic pot is perfect for both indoor and outdoor plants. It features a drainage hole for proper water flow, a sleek glazed finish, and is frost-resistant. Ideal for succulents, herbs, and decorative plants.", 100, 12.00, 2.50,True,[1], ["All", "Pots"]),
 Product("Garden Gloves - Size L", "Protect your hands while gardening with these durable, water-resistant gloves. Perfect for digging, pruning, and other gardening tasks.", 150, 8.00, 2.00, True, [1], ["All", "Gardening Tools"]),
 Product("Hanging Baskets - Set of 3", "Add a touch of elegance to your garden with these beautiful hanging baskets. Made from durable materials, they are perfect for displaying flowers, herbs, or succulents.", 80, 25.00, 10.00, True, [1], ["All", "Decorative Items"]),
 Product("Garden Fork - 1m", "A sturdy garden fork for digging and turning over soil. Perfect for preparing garden beds and removing weeds.", 100, 10.00, 3.00, True, [1], ["All", "Gardening Tools"]),
 Product("Cactus and Succulent Potting Mix", "A specially formulated potting mix designed for cacti and succulents. Promotes healthy root growth and prevents waterlogged soil.", 180, 18.00, 4.50, True, [1], ["All", "Fertilisers"]),
 Product("Fertiliser Spreader - 2m", "A handy fertiliser spreader for evenly distributing fertiliser across your garden. Perfect for large gardens or commercial use.", 140, 28.00, 12.00, True, [1], ["All", "Gardening Tools"]),
 Product("Garden Rake - 1m", "A sturdy garden rake for removing leaves and debris from your garden. Perfect for maintaining a clean and tidy garden.", 110, 12.00, 3.50, True, [1], ["All", "Gardening Tools"]),
 Product("Organic Compost - 1kg", "Made from natural ingredients, this organic compost promotes healthy plant growth and is safe for the environment.", 220, 22.00, 6.00, True, [1], ["All", "Fertilisers"]),
 Product("Garden Trowel - 30cm", "A sturdy garden trowel for planting and transplanting. Perfect for small gardens or indoor plants.", 130, 10.00, 2.50, True, [1], ["All", "Gardening Tools"]),
 Product("Hanging Baskets - Set of 5", "Add a touch of elegance to your garden with these beautiful hanging baskets. Made from durable materials, they are perfect for displaying flowers, herbs, or succulents.", 70, 35.00, 15.00, True, [1], ["All", "Decorative Items"]),
 Product("Garden Fork - 1.5m", "A sturdy garden fork for digging and turning over soil. Perfect for preparing garden beds and removing weeds.", 90, 15.00, 4.00, True, [1], ["All", "Gardening Tools"]),
 Product("Cactus and Succulent Potting Mix - 5kg", "A specially formulated potting mix designed for cacti and succulents. Promotes healthy root growth and prevents waterlogged soil.", 160, 45.00, 20.00, True, [1], ["All", "Fertilisers"]),
 Product("Patio Set - 6 Piece", "Add a touch of style to your patio with this beautiful 6-piece set. Includes a table, chairs, and a parasol.", 50, 60.00, 30.00, True, [1], ["All", "Decorative Items"]),
 Product("Fertiliser Spreader - 3m", "A handy fertiliser spreader for evenly distributing fertiliser across your garden. Perfect for large gardens or commercial use.", 120, 35.00, 15.00, True, [1], ["All", "Gardening Tools"]),
 Product("Garden Rake - 1.5m", "A sturdy garden rake for removing leaves and debris from your garden. Perfect for maintaining a clean and tidy garden.", 100, 18.00, 5.00, True, [1], ["All", "Gardening Tools"]),
 Product("Organic Fertiliser - 5kg", "This organic fertiliser is made from our food waste compost. It contains no chemical, contains no harmful pathogens, improves soil organic matter, serves as a strong foundation to bare soil, is suitable for all plants, creates savings for users,has a high NPK value and no offensive odour.", 200, 55.00, 25.00, True, [1], ["All", "Fertilisers"]),
 Product("Garden Trowel - 40cm", "A sturdy garden trowel for planting and transplanting. Perfect for small gardens or indoor plants.", 150, 15.00, 4.00, True, [1], ["All", "Gardening Tools"]),
 Product("Hanging Baskets - Set of 10", "Add a touch of elegance to your garden with these beautiful hanging baskets. Made from durable materials, they are perfect for displaying flowers, herbs, or succulents.", 60, 70.00, 35.00, True, [1], ["All", "Decorative Items"]),
 Product("Garden Fork - 2m", "A sturdy garden fork for digging and turning over soil. Perfect for preparing garden beds and removing weeds.", 80, 20.00, 6.00, True, [1], ["All", "Gardening Tools"]),
 Product("Cactus and Succulent Potting Mix - 10kg", "A specially formulated potting mix designed for cacti and succulents. Promotes healthy root growth and prevents waterlogged soil.", 180, 80.00, 40.00, True, [1], ["All", "Fertilisers"]),
 Product("Patio Set - 8 Piece", "Add a touch of style to your patio with this beautiful 8-piece set. Includes a table, chairs, and a parasol.", 40, 80.00, 40.00, True, [1], ["All", "Decorative Items"]),
 Product("Fertiliser Spreader - 4m", "A handy fertiliser spreader for evenly distributing fertiliser across your garden. Perfect for large gardens or commercial use.", 0, 40.00, 18.00, True, [1], ["All", "Gardening Tools"])]


def product_insert_to_db(product_list):
    db = shelve.open('storage.db', 'c')

    try:
        products_dict  = db['Products']
    except:
        print('Error in retrieving Products from storage.db')
        db["Products"] = {}
        products_dict = db['Products']
    if len(products_dict) < 5:
        for product in product_list:
            products_dict[product.get_product_id()] = product
            db['Products'] = products_dict
        print('Products created!')
    else:
        print('Products already exist!')
    db.close()
    
categories = [("All", "All"),("Fertiliser", "Fertiliser"),("Seeds", "Seeds"),
              ("Tools", "Gardening Tools"),("Pots", "Pots & Planters")]

def categories_insert_to_db(categories):
    db = shelve.open('storage.db', 'c')
    categories_dict = {}
    try:
        categories_dict  = db['Categories']
    except:
        print('Error in retrieving Categories from storage.db')
        db["Categories"] = {}
        categories_dict = db['Categories']
    if len(categories_dict) < 3:
        for val, label in categories:
            categories_dict[val] = label
        db['Categories'] = categories_dict
        print('Categories created!')
    else:
        print('Categories already exist!')
    db.close()
        
def image_insert_to_db():
    db = shelve.open('storage.db', 'c')
    try:
        images_dict  = db['Images']
    except:
        print('Error in retrieving Images from storage.db')
        db["Images"] = {}
        images_dict = db['Images']
    if len(images_dict) < 1:
        db['Images'] = {1: "images/default_product.png"}
        print('Images created!')
    else:
        print('Images already exist!')
    db.close()

    
user_list = [
    User(1, "admin1", "admin1@wf.com", "123", True),
    User(2, "bob", "bob@nyp.com", "123", False),
    User(3, "charlie", "charlie@gmail.com", "123", False),
    User(4, "david", "david@nyp.com", "123", False),
    User(5, "eva", "eva@nyp.com", "123", False),
    User(6, "frank", "frank@nyp.com", "123", False),
    User(7, "grace", "grace@gmail.com", "123", False),
    User(8, "henry", "henry@nyp.com", "123", False),
    User(9, "isabella", "isabella@nyp.com", "123", False),
    User(10, "jack", "jack@yahoo.com", "123", False)
]

def user_insert_to_db(user_list):
    db = shelve.open('storage.db', 'c')

    try:
        users_dict = db['Users']
    except KeyError:
        print('Error in retrieving Users from storage.db')
        db["Users"] = {}
        users_dict = db['Users']

    if len(users_dict) < 5:
        for user in user_list:
            users_dict[user.get_user_id()] = user
        db['Users'] = users_dict
        print('Users created!')
    else:
        print('Users already exist!')
    
    db.close()
    
stock_list = [
    Stock(1, 50, "2024-11-05"),
    Stock(2, 40, "2024-11-15"),
    Stock(3, 30, "2024-12-01"),
    Stock(4, 25, "2024-12-10"),
    Stock(5, 60, "2024-12-20"),
    Stock(1, 55, "2024-12-03"),
    Stock(2, 45, "2024-12-15"),
    Stock(1, 48, "2025-02-10"),
    Stock(1, 50, "2025-02-11"),
    Stock(2, 35, "2025-02-18"),
    Stock(3, 55, "2025-02-25"),
    Stock(4, 60, "2025-03-05"),
    Stock(5, 70, "2025-03-12"),
    Stock(1, 55, "2025-03-20"),
    Stock(2, 40, "2025-03-28"),
    Stock(3, 45, "2025-04-07"),
    Stock(4, 500, "2025-04-15"),  # Outlier: Unusually high quantity
    Stock(5, 65, "2025-04-25"),

]


for stock in stock_list[:-10]:
    stock.confirmed()
def stock_insert_to_db(stock_list):
    db = shelve.open('storage.db', 'c')
    stock_dict = {}
    try:
        stock_dict = db['Stock']
    except KeyError:
        print('Error in retrieving Stock from storage.db')
        db["Stock"] = {}
        stock_dict = db['Stock']
    if len(stock_dict) < 3:
        for stock in stock_list:
            stock_dict[stock.get_stock_id()] = stock
        db['Stock'] = stock_dict
        print('Stock created!')
    else:
        print('Stock already exist!')
        
    db.close()

rating_list = [
    Review("jack", 5, "Excellent product!", 2, "2025-02-10"),
    Review("frank", 3, "Decent, but could be better.", 2, "2025-02-12"),

    Review("grace", 4, "Works well, satisfied!", 14, "2025-02-15"),
    Review("henry", 2, "Not what I expected.", 14, "2025-02-17"),

    Review("isabella", 5, "Amazing! Highly recommend.", 25, "2025-03-05"),
    Review("david", 1, "Terrible experience.", 25, "2025-03-07"),

    Review("eva", 3, "It's okay, nothing special.", 26, "2025-03-10"),
    Review("charlie", 2, "Had some issues, not the best.", 26, "2025-03-12"),

    Review("bob", 4, "Pretty good overall!", 4, "2025-03-20"),
    Review("henry", 5, "Exceeded my expectations!", 4, "2025-03-22"),
]

def review_insert_to_db(rating_list):
    db = shelve.open('storage.db', 'c')
    rating_dict = {}
    try:
        rating_dict = db['Reviews']
    except KeyError:
        print('Error in retrieving Reviews from storage.db')
        db["Reviews"] = {}
        rating_dict = db['Reviews']
    if len(rating_dict) < 3:
        for rating in rating_list:
            rating_dict[rating.get_review_id()] = rating
        db['Reviews'] = rating_dict
        print('Reviews created!')
    else:
        print('Reviews already exist!')
        
    db.close()



# Modify insert_all to include user insertion
def insert_all():
    product_insert_to_db(product_list)
    categories_insert_to_db(categories)
    image_insert_to_db()
    user_insert_to_db(user_list)
    stock_insert_to_db(stock_list)
    review_insert_to_db(rating_list)
    