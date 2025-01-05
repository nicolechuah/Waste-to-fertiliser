from flask import Flask, render_template, request, redirect, url_for
from Product import Product
from forms import ProductForm
import shelve



app = Flask(__name__)

@app.route('/')
def home():
    db = shelve.open('storage.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('home.html', products_list=products_list, title = "Products")


@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/join-us')
def join_us():
    return render_template('join-us.html')

@app.route('/create-product', methods=['GET', 'POST'])
def create_product():
    create_product = ProductForm(request.form)
    if request.method == 'POST' and create_product.validate():
        product_dict = {}
        db = shelve.open('storage.db', 'c')
        
        try:
            product_dict = db['Products']
            product_id = db['ProductIDs']
            Product.product_id = product_id
            
        except:
            print("Error in retrieving Products from storage.db")
        product = Product(create_product.name.data, create_product.description.data, create_product.qty.data, 
                          create_product.selling_price.data, create_product.cost_price.data, create_product.in_stock.data)
        product_dict[product.get_product_id()] = product
        db['Products'] = product_dict
        db['ProductIDs'] = Product.product_id
        db.close()
        print(product)
        
        return redirect(url_for('product_management'))
    return render_template('create-product.html', form=create_product, title = "Create Product")

@app.route('/product-management')
def product_management():
    products_dict = {}
    db = shelve.open('storage.db', 'r')
    
    products_dict = db['Products']
    db.close()
    
    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)
    return render_template('product-management.html', products_list=products_list, title = "Manage Products")



if __name__ == '__main__':
    app.run(debug=True)
