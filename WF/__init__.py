import secrets, os
from flask import Flask, render_template, request, redirect, url_for
from Product import Product
from forms import ProductForm
import shelve



app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/images"

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
    # create object of ProductForm class
    
    if request.method == 'POST' and create_product.validate():
        image = request.files['image']
        if image:
            saved_image = save_image(image)
        else:
            saved_image = "default_product.png"
        
        product_dict = {}
        db = shelve.open('storage.db', 'c')
        
        try:
            product_dict = db['Products']
            product_id = db['ProductIDs']
            Product.product_id = product_id
            
        except:
            print("Error in retrieving Products from storage.db")
        product = Product(create_product.name.data, create_product.description.data, create_product.qty.data, 
                          create_product.selling_price.data, create_product.cost_price.data, create_product.in_stock.data, saved_image)
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

@app.route('/update-product/<int:id>/', methods=['POST', 'GET'])
def update_product(id):
    update_product = ProductForm(request.form)
    # create object of ProductForm class
    if request.method == 'POST' and update_product.validate(): # if update is valid
        products_dict = {}
        db = shelve.open('storage.db', 'w')
        products_dict = db['Products']
        product = products_dict.get(id)
        
        # if image is uploaded, save it
        image = request.files['image']
        if image:
            saved_image = save_image(image)
            delete_image(product.get_image())
        else:
            saved_image = product.get_image()
        product.set_name(update_product.name.data)
        product.set_description(update_product.description.data)
        product.set_qty(update_product.qty.data)
        product.set_selling_price(update_product.selling_price.data)
        product.set_cost_price(update_product.cost_price.data)
        product.set_in_stock(update_product.in_stock.data)
        product.set_image(saved_image)
        db['Products'] = products_dict
        db.close()
        return redirect(url_for('product_management'))
    else: # for the get request - preload the page with existing details
          # idk why but theres type error if i dont fill it?
        products_dict = {}
        db = shelve.open('storage.db', 'r')
        products_dict = db['Products']
        db.close()
        
        # populate form with existing data
        product = products_dict.get(id)
        update_product.name.data = product.get_name()
        update_product.image.data = product.get_image()
        update_product.description.data = product.get_description()
        update_product.qty.data = product.get_qty()
        update_product.selling_price.data = product.get_selling_price()
        update_product.cost_price.data = product.get_cost_price()
        update_product.in_stock.data = product.get_in_stock()
        
        return render_template('update-product.html', form=update_product,
                               title = "Update Product", product = product)
@app.route('/delete-product/<int:id>', methods=['POST'])
def delete_product(id):
    # stored variable id is passed from delete button @ product-management
    products_dict = {}
    db = shelve.open('storage.db', 'w')
    products_dict = db['Products']
    
    # Delete the image stored
    product = products_dict.get(id)
    delete_image(product.get_image())
    
    products_dict.pop(id)
    db['Products'] = products_dict
    db.close()
    return redirect(url_for('product_management'))

## Helper functions ##
# SAVE IMAGE #
def save_image(image):
        random_hex = secrets.token_hex(8) #randomize filename
        f_name, f_ext = os.path.splitext(image.filename) #split filename and extension
        image_fn = random_hex + f_ext #combine random hex and extension
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_fn) #combine root path and image path
        image.save(image_path) #save image to path, save function is under the werkzeug library
        return image_fn
    
    
def delete_image(image):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image)
    if os.path.exists(image_path) and image != "default_product.png":
        os.remove(image_path)

if __name__ == '__main__':
    app.run(debug=True)
