from Product import Product
import shelve

product_list = [Product("Organic Fertiliser - 100g", "This organic fertiliser: contains no chemical, contains no harmful pathogens, improves soil organic matter, serves as a strong foundation to bare soil, is suitable for all plants, creates savings for users,has a high NPK value and no offensive odour.",500,3.00, 0.50, True,[1],["All", "Fertiliser"]), 
 Product("Sunflower seeds", "These sunflower seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 50-60 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Compost Bin", "This compost bin is made of durable plastic and is suitable for composting kitchen waste. It has a capacity of 50 litres and is easy to assemble.",50,20.00, 5.00, True,[1],["All", "Tools"]), 
 Product("Vegetable Seeds", "These vegetable seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 30-40 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Gloves", "These garden gloves are made of durable rubber and are suitable for gardening. They have a grip on the palm and are easy to clean.",50,10.00, 2.00, True,[1],["All", "Tools"]), 
 Product("Fruit Tree Seeds", "These fruit tree seeds are easy to grow and suitable for beginners. It contains 10 seeds in a packet, with 60-90 days to maturity.",30,4.80, 1.50, True,[1],["All", "Seeds"]), 
 Product("Herb Seeds", "These herb seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 20-30 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Rake", "This garden rake is made of durable metal and is suitable for gardening. It has a sturdy handle and is easy to clean.",50,15.00, 3.00, True,[1],["All", "Tools"]), 
 Product("Organic Fertiliser - 200g", "This organic fertiliser: contains no chemical, contains no harmful pathogens, improves soil organic matter, serves as a strong foundation to bare soil, is suitable for all plants, creates savings for users,has a high NPK value and no offensive odour.",500,3.50, 0.60, True,[1],["All", "Fertiliser"]), 
 Product("Tomato Seeds", "These tomato seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 60-90 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Fork", "This garden fork is made of durable metal and is suitable for gardening. It has a sturdy handle and is easy to clean.",50,15.00, 3.00, True,[1],["All", "Tools"]), 
 Product("Compost Tea Fertiliser", "This compost tea fertiliser is made from compost tea and is suitable for all plants. It has a high NPK value and is easy to use.",50,10.00, 2.00, True,[1],["All", "Fertiliser"]), 
 Product("Cucumber Seeds", "These cucumber seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 50-60 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Hoe", "This garden hoe is made of durable metal and is suitable for gardening. It has a sturdy handle and is easy to clean.",50,15.00, 3.00, True,[1],["All", "Tools"]), 
 Product("Organic Fertiliser - 500g", "This organic fertiliser: contains no chemical, contains no harmful pathogens, improves soil organic matter, serves as a strong foundation to bare soil, is suitable for all plants, creates savings for users,has a high NPK value and no offensive odour.",500,4.00, 0.80, True,[1],["All", "Fertiliser"]), 
 Product("Carrot Seeds", "These carrot seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 60-90 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Pruning Shears", "These garden pruning shears are made of durable metal and are suitable for pruning plants. They have a sharp blade and are easy to clean.",50,20.00, 4.00, True,[1],["All", "Tools"]), 
 Product("Fertiliser Injector", "This fertiliser injector is made of durable plastic and is suitable for injecting fertiliser into soil. It has a capacity of 20 litres and is easy to assemble.",50,25.00, 6.00, True,[1],["All", "Tools"]), 
 Product("Pepper Seeds", "These pepper seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 60-90 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Rake with Handle", "This garden rake with handle is made of durable metal and is suitable for gardening. It has a sturdy handle and is easy to clean.",50,20.00, 4.00, True,[1],["All", "Tools"]), 
 Product("Organic Fertiliser - 1kg", "This organic fertiliser: contains no chemical, contains no harmful pathogens, improves soil organic matter, serves as a strong foundation to bare soil, is suitable for all plants, creates savings for users,has a high NPK value and no offensive odour.",500,5.00, 1.00, True,[1],["All", "Fertiliser"]), 
 Product("Cabbage Seeds", "These cabbage seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 60-90 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Trowel", "This garden trowel is made of durable metal and is suitable for gardening. It has a sturdy handle and is easy to clean.",50,15.00, 3.00, True,[1],["All", "Tools"]), 
 Product("Spinach Seeds", "These spinach seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 20-30 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Pruning Saw", "This garden pruning saw is made of durable metal and is suitable for pruning plants. It has a sharp blade and is easy to clean.",50,25.00, 5.00, True,[1],["All", "Tools"]), 
 Product("Fertiliser Injector with Handle", "This fertiliser injector with handle is made of durable plastic and is suitable for injecting fertiliser into soil. It has a capacity of 20 litres and is easy to assemble.",50,35.00, 8.00, True,[1],["All", "Tools"]), 
 Product("Broccoli Seeds", "These broccoli seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 60-90 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]), 
 Product("Garden Rake with Wheels", "This garden rake with wheels is made of durable metal and is suitable for gardening. It has a sturdy handle and is easy to clean.",50,25.00, 5.00, True,[1],["All", "Tools"]), 
 Product("Organic Fertiliser - 2kg", "This organic fertiliser: contains no chemical, contains no harmful pathogens, improves soil organic matter, serves as a strong foundation to bare soil, is suitable for all plants, creates savings for users,has a high NPK value and no offensive odour.",500,6.00, 1.20, True,[1],["All", "Fertiliser"]), 
 Product("Kale Seeds", "These kale seeds are easy to grow and suitable for beginners. It contains 20 seeds in a packet, with 60-90 days to maturity.",30,3.60, 1.00, True,[1],["All", "Seeds"]),
 Product("Ceramic Pot - 8 inch", "This durable ceramic pot is perfect for both indoor and outdoor plants. It features a drainage hole for proper water flow, a sleek glazed finish, and is frost-resistant. Ideal for succulents, herbs, and decorative plants.", 100, 12.00, 2.50,True,[1], ["All", "Pots"]),
 Product("Stainless Steel Watering Can - 1.5L", "A sleek, rust-resistant stainless steel watering can with a long spout for precise watering. Suitable for indoor and outdoor plants, offering both style and functionality.", 50, 15.00,3.00, True, [1], ["All", "Watering Systems"]),
 Product("Garden Gloves - Size L", "Protect your hands while gardening with these durable, water-resistant gloves. Perfect for digging, pruning, and other gardening tasks.", 150, 8.00, 2.00, True, [1], ["All", "Gardening Tools"]),
 Product("Hanging Baskets - Set of 3", "Add a touch of elegance to your garden with these beautiful hanging baskets. Made from durable materials, they are perfect for displaying flowers, herbs, or succulents.", 80, 25.00, 10.00, True, [1], ["All", "Decorative Items"]),
 Product("Self-Watering Planters - 2 Pack", "Keep your plants hydrated with these innovative self-watering planters. Perfect for busy gardeners or those who tend to forget to water their plants.", 120, 30.00, 15.00, True, [1], ["All", "Watering Systems"]),
 Product("Garden Fork - 1m", "A sturdy garden fork for digging and turning over soil. Perfect for preparing garden beds and removing weeds.", 100, 10.00, 3.00, True, [1], ["All", "Gardening Tools"]),
 Product("Cactus and Succulent Potting Mix", "A specially formulated potting mix designed for cacti and succulents. Promotes healthy root growth and prevents waterlogged soil.", 180, 18.00, 4.50, True, [1], ["All", "Fertilisers"]),
 Product("Garden Hose - 20m", "A durable, kink-resistant garden hose perfect for watering your garden. Made from high-quality materials, it is resistant to UV light and weathering.", 90, 35.00, 18.00, True, [1], ["All", "Watering Systems"]),
 Product("Patio Set - 4 Piece", "Add a touch of style to your patio with this beautiful 4-piece set. Includes a table, chairs, and a parasol.", 60, 40.00, 20.00, True, [1], ["All", "Decorative Items"]),
 Product("Fertiliser Spreader - 2m", "A handy fertiliser spreader for evenly distributing fertiliser across your garden. Perfect for large gardens or commercial use.", 140, 28.00, 12.00, True, [1], ["All", "Gardening Tools"]),
 Product("Garden Rake - 1m", "A sturdy garden rake for removing leaves and debris from your garden. Perfect for maintaining a clean and tidy garden.", 110, 12.00, 3.50, True, [1], ["All", "Gardening Tools"]),
 Product("Organic Compost - 1kg", "Made from natural ingredients, this organic compost promotes healthy plant growth and is safe for the environment.", 220, 22.00, 6.00, True, [1], ["All", "Fertilisers"]),
 Product("Garden Trowel - 30cm", "A sturdy garden trowel for planting and transplanting. Perfect for small gardens or indoor plants.", 130, 10.00, 2.50, True, [1], ["All", "Gardening Tools"]),
 Product("Hanging Baskets - Set of 5", "Add a touch of elegance to your garden with these beautiful hanging baskets. Made from durable materials, they are perfect for displaying flowers, herbs, or succulents.", 70, 35.00, 15.00, True, [1], ["All", "Decorative Items"]),
 Product("Self-Watering Planters - 3 Pack", "Keep your plants hydrated with these innovative self-watering planters. Perfect for busy gardeners or those who tend to forget to water their plants.", 100, 40.00, 20.00, True, [1], ["All", "Watering Systems"]),
 Product("Garden Fork - 1.5m", "A sturdy garden fork for digging and turning over soil. Perfect for preparing garden beds and removing weeds.", 90, 15.00, 4.00, True, [1], ["All", "Gardening Tools"]),
 Product("Cactus and Succulent Potting Mix - 5kg", "A specially formulated potting mix designed for cacti and succulents. Promotes healthy root growth and prevents waterlogged soil.", 160, 45.00, 20.00, True, [1], ["All", "Fertilisers"]),
 Product("Garden Hose - 30m", "A durable, kink-resistant garden hose perfect for watering your garden. Made from high-quality materials, it is resistant to UV light and weathering.", 80, 50.00, 25.00, True, [1], ["All", "Watering Systems"]),
 Product("Patio Set - 6 Piece", "Add a touch of style to your patio with this beautiful 6-piece set. Includes a table, chairs, and a parasol.", 50, 60.00, 30.00, True, [1], ["All", "Decorative Items"]),
 Product("Fertiliser Spreader - 3m", "A handy fertiliser spreader for evenly distributing fertiliser across your garden. Perfect for large gardens or commercial use.", 120, 35.00, 15.00, True, [1], ["All", "Gardening Tools"]),
 Product("Garden Rake - 1.5m", "A sturdy garden rake for removing leaves and debris from your garden. Perfect for maintaining a clean and tidy garden.", 100, 18.00, 5.00, True, [1], ["All", "Gardening Tools"]),
 Product("Organic Compost - 5kg", "Made from natural ingredients, this organic compost promotes healthy plant growth and is safe for the environment.", 200, 55.00, 25.00, True, [1], ["All", "Fertilisers"]),
 Product("Garden Trowel - 40cm", "A sturdy garden trowel for planting and transplanting. Perfect for small gardens or indoor plants.", 150, 15.00, 4.00, True, [1], ["All", "Gardening Tools"]),
 Product("Hanging Baskets - Set of 10", "Add a touch of elegance to your garden with these beautiful hanging baskets. Made from durable materials, they are perfect for displaying flowers, herbs, or succulents.", 60, 70.00, 35.00, True, [1], ["All", "Decorative Items"]),
 Product("Self-Watering Planters - 4 Pack", "Keep your plants hydrated with these innovative self-watering planters. Perfect for busy gardeners or those who tend to forget to water their plants.", 90, 50.00, 25.00, True, [1], ["All", "Watering Systems"]),
 Product("Garden Fork - 2m", "A sturdy garden fork for digging and turning over soil. Perfect for preparing garden beds and removing weeds.", 80, 20.00, 6.00, True, [1], ["All", "Gardening Tools"]),
 Product("Cactus and Succulent Potting Mix - 10kg", "A specially formulated potting mix designed for cacti and succulents. Promotes healthy root growth and prevents waterlogged soil.", 180, 80.00, 40.00, True, [1], ["All", "Fertilisers"]),
 Product("Garden Hose - 40m", "A durable, kink-resistant garden hose perfect for watering your garden. Made from high-quality materials, it is resistant to UV light and weathering.", 70, 65.00, 30.00, True, [1], ["All", "Watering Systems"]),
 Product("Patio Set - 8 Piece", "Add a touch of style to your patio with this beautiful 8-piece set. Includes a table, chairs, and a parasol.", 40, 80.00, 40.00, True, [1], ["All", "Decorative Items"]),
 Product("Fertiliser Spreader - 4m", "A handy fertiliser spreader for evenly distributing fertiliser across your garden. Perfect for large gardens or commercial use.", 110, 40.00, 18.00, True, [1], ["All", "Gardening Tools"])]


def insert_to_db(product_list):
    db = shelve.open('storage.db')
    try:
        products_dict  = db['Products']
    except:
        print('Error in retrieving Products from storage.db')
        db["Products"] = {}
        products_dict = db['Products']
    for product in product_list:
        products_dict[product.get_product_id()] = product
    db['Products'] = products_dict
    db.close()
    