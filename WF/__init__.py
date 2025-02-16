from flask import Flask, render_template, url_for, flash, redirect, request, session,send_file,jsonify
from AllForms import RegistrationForm, LoginForm, AccountForm, ResetPasswordForm, ProductForm, UserFWF, CheckoutForm, PaymentForm
from AllForms import CollectFood,ReviewForm, InventoryForm
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from datetime import datetime, timedelta
import shelve, User, initial_settings, subprocess ,os, random, secrets
from PIL import Image
import pandas as pd
from datetime import datetime
from werkzeug.utils import secure_filename
from Product import Product
from Review import Review
from Stock import Stock
import shelve
from Fwfuser import FWFUser
from Collect import Collect
from Image import Image
from image_search import search_by_image 


app = Flask(__name__)

app.config['SECRET_KEY'] = 'd6691973382147ed2b8724aa19eb0720'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images')
app.config['MAX_CONTENT_LENGTH'] = 10 *1024 * 1024
TEMP_FOLDER = os.path.join(app.root_path, 'temp') # temp folder for file uploads
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)
ALLOW_INIT_ADMIN = True  # Set to True to allow the creation of an initial admin account



@app.route('/', defaults={'category': None}, methods=['GET', 'POST'])
@app.route('/category/<category>', methods=['GET', 'POST'])
def home(category):
    try:
        db = shelve.open('storage.db', 'r')
        products_dict = db['Products']
        cat_dict = db['Categories']
    except:
        print("Error in retrieving data from storage.db")
        db = shelve.open('storage.db', 'c')
        db['Products'] = {}
        products_dict = db['Products']
        db['Images'] = {}
        image_dict = db['Images']
        db['Categories'] = {}
        cat_dict = db['Categories']
    db.close()

    # Create category list
    cat_list = []
    for val, label in cat_dict.items():
        cat_list.append((val, label))


    products_list = []
    if category is None or category == "All":
        for key in products_dict:
            product = products_dict.get(key)
            product.display_image = product.display_first_img()
            products_list.append(product)
    else:
        for key in products_dict:
            product = products_dict.get(key)
            list_of_cat = product.get_category()
            for cat in list_of_cat:
                if cat == category:
                    product.display_image = product.display_first_img()
                    products_list.append(product)
                    break
    search = request.args.get('q', '').lower().strip()
    search_list = []
    if search:
        for product in products_list:
            if search in product.get_name().lower():
                search_list.append(product)
    products_list = search_list if search else products_list
    # partial response handling 
    if request.headers.get('HX-Request'):
        return render_template('includes/home_partial.html', products_list=products_list, cat_list=cat_list, title="Home")
    # uses a partial page meaing that it only updates the part of the page that is needed by id (hx-target)

    # Process POST request for adding product to cart
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        unit_price = float(request.form.get('unit_price', 0))
        if product_name:
            try:
                quantity = 1
                with shelve.open('storage.db', writeback=True) as db:
                    if 'cart' not in db:
                        db['cart'] = {'items': []}
                    cart_items = db['cart']['items']
                    found = False
                    for item in cart_items:
                        if item['name'] == product_name:
                            item['quantity'] += quantity
                            item['total_price'] = item['unit_price'] * item['quantity']
                            found = True
                            break
                    if not found:
                        cart_items.append({
                            'name': product_name,
                            'unit_price': unit_price,
                            'quantity': quantity,
                            'total_price': unit_price * quantity
                        })
                    db['cart']['items'] = cart_items
                flash(f"{product_name} successfully added to cart!", 'success')
            except Exception as e:
                flash(f"Error adding product to cart: {e}", 'danger')

    # Set the page title depending on whether a category is selected
    if category is None or category == "All":
        title = "Home"
    else:
        title = category

    return render_template('home.html', products_list=products_list, cat_list=cat_list, title=title)

@app.route('/filter/<sort_key>', methods=['GET', 'POST'], endpoint='filter')
def filter_products(sort_key):
    # Open the shelve database and get products and categories
    try:
        db = shelve.open('storage.db', 'r')
        products_dict = db.get('Products', {})
        cat_dict = db.get('Categories', {})
    except Exception as e:
        print("Error retrieving data from storage.db:", e)
        db = shelve.open('storage.db', 'c')
        db['Products'] = {}
        products_dict = db['Products']
        db['Images'] = {}
        db['Categories'] = {}
        cat_dict = db['Categories']
    db.close()
    cat_list = []
    for val, label in cat_dict.items():
        cat_list.append((val, label))

 
    products_list = []
    for prod_key in products_dict:
        product = products_dict.get(prod_key)
        product.display_image = product.display_first_img()
        products_list.append(product)

    if sort_key == 'ratings':
        def get_rating(product):
            try:
                return float(product.get_average_rating())
            except:
                return 0.0
        products_list.sort(key=get_rating, reverse=True)
        title = "Products by Rating"
    elif sort_key == 'hightolow':
        products_list.sort(key=lambda product: product.get_selling_price(), reverse=True)
        title = "Products: Price High to Low"
    elif sort_key == 'lowtohigh':
        products_list.sort(key=lambda product: product.get_selling_price())
        title = "Products: Price Low to High"
    else:
        title = "Products"
        products_list.sort(key=lambda product: product.get_name())
# Process POST request for adding product to cart
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        unit_price = float(request.form.get('unit_price', 0))
        if product_name:
            try:
                quantity = 1
                with shelve.open('storage.db', writeback=True) as db:
                    if 'cart' not in db:
                        db['cart'] = {'items': []}
                    cart_items = db['cart']['items']
                    found = False
                    for item in cart_items:
                        if item['name'] == product_name:
                            item['quantity'] += quantity
                            item['total_price'] = item['unit_price'] * item['quantity']
                            found = True
                            break
                    if not found:
                        cart_items.append({
                            'name': product_name,
                            'unit_price': unit_price,
                            'quantity': quantity,
                            'total_price': unit_price * quantity
                        })
                    db['cart']['items'] = cart_items
                flash(f"{product_name} successfully added to cart!", 'success')
            except Exception as e:
                flash(f"Error adding product to cart: {e}", 'danger')
    return render_template('home.html', products_list=products_list, cat_list=cat_list, title=title)
                        
@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        unit_price = float(request.form.get('unit_price', 0))

        if product_name:
            try:
                quantity = 1
                with shelve.open('storage.db', writeback=True) as db:
                    if 'cart' not in db:
                        db['cart'] = {'items': []}

                    cart_items = db['cart']['items']

                    for item in cart_items:
                        if item['name'] == product_name:
                            item['quantity'] += quantity
                            item['total_price'] = item['unit_price'] * item['quantity']
                            break
                    else:
                        cart_items.append({
                            'name': product_name,
                            'unit_price': unit_price,
                            'quantity': quantity,
                            'total_price': unit_price * quantity
                        })

                    db['cart']['items'] = cart_items
                flash(f"{product_name} successfully added to cart!", 'success')
            except Exception as e:
                flash(f"Error adding product to cart: {e}", 'danger')

    return render_template('products.html', title="Products")

@app.route('/buy-now', methods=['POST'])
def buy_now():
    product_name = request.form.get('product_name')
    unit_price = float(request.form.get('unit_price', 0))

    if product_name:
        try:
            quantity = 1
            with shelve.open('storage.db', writeback=True) as db:
                if 'cart' not in db:
                    db['cart'] = {'items': []}

                cart_items = db['cart']['items']

                for item in cart_items:
                    if item['name'] == product_name:
                        item['quantity'] += quantity
                        item['total_price'] = item['unit_price'] * item['quantity']
                        break
                else:
                    cart_items.append({
                        'name': product_name,
                        'unit_price': unit_price,
                        'quantity': quantity,
                        'total_price': unit_price * quantity
                    })

                db['cart']['items'] = cart_items
            
            flash(f"{product_name} successfully added to cart!", 'success')
            return redirect(url_for('checkout'))
        except Exception as e:
            flash(f"Error processing request: {e}", 'danger')
    
    return redirect(url_for('home'))

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart_items = []
    overall_price = 0

    with shelve.open('storage.db', writeback=True) as db:
        if 'cart' in db:
            cart_items = db['cart']['items']

        if request.method == 'POST':
            if 'increase' in request.form:
                product_name = request.form['increase']
                for item in cart_items:
                    if item['name'] == product_name:
                        item['quantity'] += 1
                        item['total_price'] = item['unit_price'] * item['quantity']
                        break

            elif 'decrease' in request.form:
                product_name = request.form['decrease']
                for item in cart_items:
                    if item['name'] == product_name:
                        if item['quantity'] > 1:
                            item['quantity'] -= 1
                            item['total_price'] = item['unit_price'] * item['quantity']
                        else:
                            flash("Quantity cannot be less than 1. Use 'Remove' to delete the item.", 'warning')
                        break

            elif 'remove' in request.form:
                product_name = request.form['remove']
                cart_items = [item for item in cart_items if item['name'] != product_name]
                flash(f"{product_name} removed from cart.", 'info')

            db['cart']['items'] = cart_items

        overall_price = sum(item['total_price'] for item in cart_items)

    return render_template("cart.html", cart_items=cart_items, overall_price=overall_price, title="Shopping Cart")

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()
    if form.validate_on_submit():
        delivery_data = {
            'full_name': form.full_name.data,
            'phone_number': form.phone_number.data,
            'postal_code': form.postal_code.data,
            'address': form.address.data,
            'unit_number': form.unit_number.data
        }
        with shelve.open('storage.db', writeback=True) as db:
            if 'delivery' not in db:
                db['delivery'] = {'records': []}
            db['delivery']['records'].append(delivery_data)
        return redirect(url_for('payment'))
    return render_template('checkout.html', form=form, title="Checkout")

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    form = PaymentForm()
    if form.validate_on_submit():
        payment_data = {
            'cardholder_name': form.cardholder_name.data,
            'card_number': form.card_number.data,
            'expiry_date': form.expiry_date.data,
            'cvv': form.cvv.data
        }
        with shelve.open('storage.db', writeback=True) as db:
            if 'payment' not in db:
                db['payment'] = {'records': []}
            db['payment']['records'].append(payment_data)

            if 'complete' not in db:
                db['complete'] = {'items': []}
            db['complete']['items'].extend(db.get('cart', {}).get('items', []))
            db['cart'] = {'items': []}

        flash("Payment successfully processed!", 'success')
        return redirect(url_for('home'))
    return render_template('payment.html', form=form, title="Payment")

@app.route('/user')
def user():
    with shelve.open('storage.db', 'r') as db:
        complete_data = db.get('complete', {}).get('items', [])
        delivery_data = db.get('delivery', {}).get('records', [])
        payment_data = db.get('payment', {}).get('records', [])

    return render_template('user.html', complete_data=complete_data, delivery_data=delivery_data, payment_data=payment_data, title="User Data")

@app.route('/edit-delivery/<int:id>', methods=['GET', 'POST'])
def edit_delivery(id):
    form = CheckoutForm()
    with shelve.open('storage.db', writeback=True) as db:
        delivery_data = db.get('delivery', {}).get('records', [])
        if id >= len(delivery_data):
            flash("Invalid delivery record.", 'danger')
            return redirect(url_for('user'))

        if form.validate_on_submit():
            delivery_data[id] = {
                'full_name': form.full_name.data,
                'phone_number': form.phone_number.data,
                'postal_code': form.postal_code.data,
                'address': form.address.data,
                'unit_number': form.unit_number.data
            }
            db['delivery']['records'] = delivery_data
            flash("Delivery details updated successfully.", 'success')
            return redirect(url_for('user'))

        form.full_name.data = delivery_data[id]['full_name']
        form.phone_number.data = delivery_data[id]['phone_number']
        form.postal_code.data = delivery_data[id]['postal_code']
        form.address.data = delivery_data[id]['address']
        form.unit_number.data = delivery_data[id].get('unit_number')

    return render_template('checkout.html', form=form, title="Edit Delivery Details")

@app.route('/edit-payment/<int:id>', methods=['GET', 'POST'])
def edit_payment(id):
    form = PaymentForm()
    with shelve.open('storage.db', writeback=True) as db:
        payment_data = db.get('payment', {}).get('records', [])
        if id >= len(payment_data):
            flash("Invalid payment record.", 'danger')
            return redirect(url_for('user'))

        if form.validate_on_submit():
            payment_data[id] = {
                'cardholder_name': form.cardholder_name.data,
                'card_number': form.card_number.data,
                'expiry_date': form.expiry_date.data,
                'cvv': form.cvv.data
            }
            db['payment']['records'] = payment_data
            flash("Payment details updated successfully.", 'success')
            return redirect(url_for('user'))

        form.cardholder_name.data = payment_data[id]['cardholder_name']
        form.card_number.data = payment_data[id]['card_number']
        form.expiry_date.data = payment_data[id]['expiry_date']
        form.cvv.data = payment_data[id]['cvv']

    return render_template('home.html', form=form, title="Edit Payment Details")


@app.route('/help')
def help():
    return render_template('help.html', title="Help")

@app.route('/join-us')
def join_us():
    return render_template('join-us.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        users_dict = {}
        db = shelve.open('storage.db', 'c')
        user_id = db.get('UserIDs', 0)
        user_id += 1

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from storage.db.")

            # Check for duplicate email
        for user in users_dict.values():
            if form.email.data == user.get_email():
                db.close()
                flash('This email is already registered. Please use a different email.', 'danger')
                return render_template('register.html', title='Register', form=form)
            
        user = User.User(
            user_id,
            form.username.data,
            form.email.data,
            form.password.data,
        )
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict
        db['UserIDs'] = user_id
        db.close()

        flash(f'Account created for {form.username.data}!', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()
        
        for user in users_dict.values():
            if form.email.data == user.get_email() and form.password.data == user.get_password(): 
                session['logged_in'] = True
                session['username'] = user.get_username()
                session['is_admin'] = user.is_admin()
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
        
        flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route("/reset_password", methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        users_dict = {}
        db = shelve.open('storage.db', 'r')
        users_dict = db['Users']
        db.close()
        
        for user in users_dict.values():
            if form.email.data == user.get_email():
                flash('An email has been sent with instructions to reset your password.', 'info')
                return redirect(url_for('login'))
            
        flash('Email not found. Please check the email entered.', 'danger')
    return render_template('reset_password.html', title='Reset Password', form=form)

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
def account():
    form = AccountForm()
    users_dict = {}
    db = shelve.open('storage.db', 'c')
    try:
        users_dict = db['Users']
    except:
        print("Error in retrieving Users from storage.db")
        db['Users'] = {}

    current_user_id = None
    current_user = None
    for user_id, user in users_dict.items():
        if user.get_username() == session['username']:
            current_user_id = user_id
            current_user = user
            break

    if not current_user:
        flash('User not found. Please log in again.', 'danger')
        return redirect(url_for('login'))

    if form.validate_on_submit():
        updated = False

        # Update username
        if form.username.data and form.username.data != current_user.get_username():
            current_user.set_username(form.username.data)
            session["username"] = form.username.data  # Sync session data
            updated = True

        # Update email
        if form.email.data and form.email.data != current_user.get_email():
            current_user.set_email(form.email.data)
            updated = True

        # Update password
        if form.password.data:
            current_user.set_password(form.password.data)
            updated = True

        # Save changes to the database
        if updated:
            users_dict[current_user_id] = current_user 
            db["Users"] = users_dict  
            db.close()  
            flash("Your account has been updated!", "success")
            return redirect(url_for("account"))
        else:
            flash("No changes were made.", "info")

    # Pre-fill the form with the current user's data for GET requests
    form.username.data = current_user.get_username()
    form.email.data = current_user.get_email()
    form.current_password.data = current_user.get_password()

    db.close()
    return render_template("account.html", title="Account", form=form, user=current_user)

@app.route("/delete_user/<int:user_id>", methods=['POST'])
def delete_user(user_id):
    if not session.get('is_admin', False):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

    db = shelve.open('storage.db', 'c')
    users_dict = db.get('Users', {})
    user = users_dict.pop(user_id, None)
    db['Users'] = users_dict
    db.close()

    if user:
        flash('User deleted successfully.', 'success')
    else:
        flash('User not found.', 'danger')

    return redirect(url_for('manage_users'))

@app.route("/edit_user/<int:user_id>", methods=['GET', 'POST'])
def edit_user(user_id):
    if not session.get('is_admin', False):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))
    
    form = AccountForm()
    db = shelve.open('storage.db', 'c')

    try:
        users_dict = db['Users']
    except KeyError:
        users_dict = {}

    # Retrieve the user by user_id
    current_user = users_dict.get(user_id)

    if not current_user:
        db.close()
        flash('User not found.', 'danger')
        return redirect(url_for('manage_users'))

    # Handle form submission
    if form.validate_on_submit():
        updated = False

        # Update username
        if form.username.data and form.username.data != current_user.get_username():
            current_user.set_username(form.username.data)
            updated = True

        # Update email
        if form.email.data and form.email.data != current_user.get_email():
            current_user.set_email(form.email.data)
            updated = True

        # Update password
        if form.password.data:
            current_user.set_password(form.password.data)
            updated = True

        # Save changes to the database
        if updated:
            users_dict[user_id] = current_user  # Save updated user
            db['Users'] = users_dict
            db.close()
            flash("User details have been updated successfully!", "success")
            return redirect(url_for("manage_users"))
        else:
            flash("No changes were made.", "info")

    # Pre-fill the form with the current user's data for GET requests
    form.username.data = current_user.get_username()
    form.email.data = current_user.get_email()
    form.current_password.data = current_user.get_password()

    db.close()
    return render_template("edit_user.html", title="Edit User", form=form, user=current_user)

@app.route('/create-product', methods=['GET', 'POST'])
def create_product():
    # Check if the current user is logged in and is an admin
    if not session.get('is_admin', False):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

    create_product = ProductForm(request.form)
    # create object of ProductForm class
    relevant_image_IDs = []
    uploaded_images = request.files.getlist('images')
    if request.method == 'POST' and create_product.validate():
        action = request.form.get('action')
        if action == 'Submit':
            db = shelve.open('storage.db', 'c')
            if len(uploaded_images) == 1 and uploaded_images[0].filename == "": # if no image uploaded
                    relevant_image_IDs.append(1)
                    try:
                        image_dict = db['Images']
                    except:
                        print("Error in retrieving Image from image.db")
                        db['Images'] = {}
                        image_dict = db['Images']
                    if image_dict.get(1) is None:
                        image_dict[1] = "images/default_product.png"
                        db['Images'] = image_dict
            else:
                for uploaded_image in request.files.getlist('images'):
                    # save the image
                    saved = Image.save_image(uploaded_image)
                    image_path = f"images/{saved}"
                    image_dict = {}
                    # assign it an ID
                    try:
                        image_dict = db['Images']
                        old_image_id = db['ImageIDs']
                        new_image_id = old_image_id + 2
                    except:
                        print("Error in retrieving Image from image.db")
                        db['ImageIDs'] = 40
                        new_image_id = db['ImageIDs'] + 2
                    # save the image using {ID: image}
                    image_dict[new_image_id] = image_path
                    db['Images'] = image_dict
                    db['ImageIDs'] = new_image_id
                    print(f"total images: {image_dict}")                                       
                    relevant_image_IDs.append(new_image_id)
            db.close()
            category = create_product.category.data
            list_of_category = ['All'] + category

            product_dict = {}
            db = shelve.open('storage.db', 'c')

            try:
                product_dict = db['Products']
                product_id = db['ProductIDs']
                Product.product_id = product_id

            except:
                print("Error in retrieving Products from storage.db")
                db['Products'] = {}
            product = Product(create_product.name.data, create_product.description.data, create_product.qty.data, 
                              create_product.selling_price.data, create_product.cost_price.data, create_product.visible.data, relevant_image_IDs,list_of_category)
            product_dict[product.get_product_id()] = product
            db['Products'] = product_dict
            db['ProductIDs'] = Product.product_id
            db.close()
            print(f"product printing {product}")
            flash(f'Product {create_product.name.data} created!', 'success')
            return redirect(url_for('product_management'))
        if action == 'generate':
            if create_product.description.data:
                response = generate_response(create_product.description.data, create_product.name.data)
                create_product.description.data = response
                flash('Description generated successfully!', 'success')
            else:
                flash('Please enter a description to generate.', 'warning')
            return render_template('create-product.html', form=create_product, title = "Create Product")
    return render_template('create-product.html', form=create_product, title = "Create Product")

def generate_response(text, product_name):
    prompt = (
    f"You are tasked with writing a product description for {product_name}, for a gardening website. "
    "Your output must be under 100 words. Write in a friendly and informative tone. "
    "If necessary, present these points as bullet points using a hyphen followed by a space at the beginning of the line. Leave a blank line for each new bullet point."
    "Do not ask questions or request further details; only output the refined description. It must be under 100 words. "
    "Original pointers: " + text + "\n include all original pointers provided above in your refined description. Include days to maturity, care insturctions, quantity in each packet, etc."
    
)

    command = f"ollama run llama3.2:3b '{prompt}'"
    print(f"Running command: {command}")
    try:
        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
        print(f"Command output: {result.stdout}")
        # The response is expected in stdout
        response = result.stdout.strip()
    except:
        response = f"Error generating response. Please ensure Ollama is installed and running and try again."

    return response



@app.route('/import-products', methods=['GET', 'POST'])
def import_products():
    if request.method == "GET":
        return render_template('import-products.html', title="Import Products")
    file = request.files['file']
    filename = secure_filename(file.filename)
    temp_file_path = os.path.join(app.root_path, 'temp', filename)
    file.save(temp_file_path)
    try:
        df = pd.read_excel(temp_file_path, engine = 'openpyxl')
        
        #counter
        stats = 0
        db = shelve.open('storage.db', 'c')
        products_dict = db.get('Products', {})
        for x, row in df.iterrows():
            name = row['Name']
            description = row['Description']
            qty = row['Quantity']
            selling_price = row['Selling Price']
            cost_price = row['Cost Price']
            visible = row['Visible']
            images = [1]
            category_string = row['Category']  # Output: "['All', 'Pots']"
            trimming = category_string[1:-1]
            category = []

            for cat in trimming.split(","):
            # remove spaces, then remove the single quotes
                cleaned_cat = cat.strip().strip("'")
                category.append(cleaned_cat)

            print(category)  # Output: ['All', 'Pots']
            print(type(category))  # Output: <class 'list'>
            
            new_product = Product(name, description, qty, selling_price, cost_price, visible, images, category)
            products_dict[new_product.get_product_id()] = new_product
            stats += 1
        db['Products'] = products_dict
        db.close()
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if request.accept_mimetypes.accept_json: 
            return jsonify({  # only becaue dropzone uses ajax, jsonify helps to return json response
                              # passes this to javascript on import-products.html
                'success': True,
                'message': f"Successfully imported {stats} products!",
                'stats': stats
            })
        else:
            flash(f"Successfully imported {stats} products!", 'success')
            return redirect(url_for('product_management'))
    except:
        if request.accept_mimetypes.accept_json:
            return jsonify({
                'success': False,
                'message': "Error importing products. Please check the file format."
            })
        else:
            flash("Error importing products. Please check the file format.", 'danger')
    return redirect(url_for('product_management'))
            

@app.route('/export-products', methods=['GET'])
def export_products():
    db = shelve.open('storage.db', 'r')
    try:
        products_dict = db['Products']
    except:
        print("Error in retrieving Products from storage.db")
        db.close()
        return redirect(url_for('product_management'))
    product_objects = []
    for key, obj in products_dict.items():
        product_objects.append(obj)
    object_info = []
    for object in product_objects:
            object_info.append({"Product ID": object.get_product_id(), 
                           "Name": object.get_name(), 
                           "Description": object.get_description(),  
                           "Selling Price": object.get_selling_price(), 
                           "Cost Price": object.get_cost_price(), 
                           "Visible": object.get_visible(), 
                           "Category": object.get_category()})
    df = pd.DataFrame(object_info)
    output_file = os.path.join(TEMP_FOLDER, 'products.xlsx')
    df.to_excel(output_file,index=False)
    db.close()
    return send_file(output_file, as_attachment=True)

@app.route("/manageUsers", methods=['GET'])
def manage_users():
    if not session.get('is_admin', False):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

    db = shelve.open('storage.db', 'r')
    users_dict = db.get('Users', {})
    db.close()

    return render_template('manageUsers.html', title="Manage Users", users=users_dict)
@app.route("/create_admin", methods=['GET', 'POST'])
def create_admin():
    # Check if the current user is logged in and is an admin
    if not session.get('is_admin', False):
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        db = shelve.open('storage.db', 'c')
        users_dict = db.get('Users', {})
        user_id = db.get('UserIDs', 0)
        user_id += 1

        # Check for duplicate email
        for user in users_dict.values():
            if form.email.data == user.get_email():
                db.close()
                flash('This email is already registered. Please use a different email.', 'danger')
                return render_template('create_admin.html', form=form)

        # Create a new admin user
        admin_user = User.User(
            user_id,
            form.username.data,
            form.email.data,
            form.password.data,
            is_admin=True  # Mark as admin
        )
        users_dict[admin_user.get_user_id()] = admin_user
        db['Users'] = users_dict
        db['UserIDs'] = user_id
        db.close()

        flash(f'Admin account created for {form.username.data}!', 'success')
        return redirect(url_for('manage_users'))

    return render_template('create_admin.html', form=form)


@app.route("/initialise_admin", methods=["GET"])
def initialise_admin():
    # Check if the initialization flag is enabled
    if not ALLOW_INIT_ADMIN:
        flash('This route is disabled for security reasons.', 'danger')
        return redirect(url_for('home'))

    db = shelve.open('storage.db', 'c')
    users_dict = db.get('Users', {})
    user_id = db.get('UserIDs', 0)
    user_id += 1

    # Check if an admin already exists
    for user in users_dict.values():
        if user.is_admin():
            db.close()
            flash('An admin account already exists.', 'danger')
            return redirect(url_for('login'))

    # Create the initial admin account
    admin = User.User(
        user_id,
        "admin",  # Username
        "admin1@wf.com",  # Email
        "12345",  # Password
        is_admin=True  # Mark as admin
    )
    users_dict[user_id] = admin
    db['Users'] = users_dict
    db['UserIDs'] = user_id
    db.close()

    flash("Admin account created successfully.", 'success')
    return redirect(url_for('login'))

@app.route('/product-management', defaults={'category': None}, methods=['GET', 'POST'])
@app.route('/product-management/category/<category>', methods=['GET', 'POST'])
def product_management(category):
    products_dict = {}
    try:
        db = shelve.open('storage.db', 'r')
    except:
        print("Error in retrieving data from storage.db")
        db = shelve.open('storage.db', 'c')

    products_dict = db['Products']
    cat_dict = db['Categories']
    cat_list = []
    for val, label in cat_dict.items():
        cat_list.append((val, label))
    db.close()
    
    # category filter
    products_list = []
    if category is None or category == "All":
        for key in products_dict:
            product = products_dict.get(key)        
            product.display_image = product.display_first_img()
            products_list.append(product)
    else:
        for key in products_dict:
            product = products_dict.get(key)
            list_of_cat = product.get_category()
            for cat in list_of_cat:
                if cat == category:
                    product.display_image = product.display_first_img()
                    products_list.append(product)
                    break
                
    # search function         
    search = request.args.get('q', '').lower().strip()
    if search:
        search_list = []
        for product in products_list: # search in name, description, and product id
            if (search in product.get_name().lower() or
                search in product.get_description().lower() or
                search in str(product.get_product_id()).lower()):
                search_list.append(product)
        products_list = search_list

    # Partial response handling using htmx
    if request.headers.get('HX-Request'):
        return render_template('includes/product_management_partial.html', 
                               products_list=products_list, 
                               cat_list=cat_list, 
                               title="Manage Products")

    return render_template('product-management.html', products_list=products_list, cat_list=cat_list, title="Manage Products")



@app.route('/inventory', methods = ['GET', 'POST'])
def inventory():
    products_dict = {}
    inventory_form = InventoryForm(request.form)
    try:
        db = shelve.open('storage.db', 'r')
    except:
        print("Error in retrieving data from storage.db")
        db = shelve.open('storage.db', 'c')
        db['Products'] = {}
    products_dict = db['Products']
    db.close()
    
    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)
    
    return render_template('inventory.html', products_list=products_list, form=inventory_form, title = "Inventory")

@app.route('/export-inventory', methods=['GET'])
def export_inventory():
    db = shelve.open('storage.db', 'r')
    try:
        products_dict = db['Products']
    except:
        print("Error in retrieving Products from storage.db")
        db.close()
        return redirect(url_for('inventory'))
    product_objects = []
    for key, obj in products_dict.items():
        product_objects.append(obj)
    object_info = []
    
    for object in product_objects:
        in_stock = True if object.get_qty() > 0 else False
        object_info.append({"Product ID": object.get_product_id(), 
                            "Name": object.get_name(),
                            "In stock" : in_stock,
                            "Quantity": object.get_qty(),})
    df = pd.DataFrame(object_info)
    output_file = os.path.join(TEMP_FOLDER, 'inventory.xlsx')
    df.to_excel(output_file,index=False)
    db.close()
    return send_file(output_file, as_attachment=True)

@app.route('/view-stock', methods=['GET', 'POST']) 
def view_stock():
    db = shelve.open('storage.db', 'r')
    stock_dict = db["Stock"]
    db.close()
    stock_list = []
    for key in stock_dict:
        stock = stock_dict.get(key)
        stock_list.append(stock)
    stock_list.reverse()
    return render_template('view-stock.html', stock_list=stock_list, title="View Stock")

@app.route('/pending-stock', methods=['GET', 'POST'])
def pending_stock():
    db = shelve.open('storage.db', 'r')
    stock_dict = db["Stock"]
    db.close()
    stock_list = []
    for key in stock_dict:
        stock = stock_dict.get(key)
        if stock.get_confirmed_status() == False:
            stock_list.append(stock)
    return render_template('pending-stock.html', stock_list=stock_list, title="Pending Stock")

@app.route('/confirm-stock/<int:product_id>/<int:stock_id>', methods=['POST'])
def confirm_stock(product_id, stock_id):
    inventory_form = InventoryForm(request.form)
    if inventory_form.validate():
       # in-memory modifications are saved.
        db = shelve.open('storage.db', 'c', writeback=True)
        products_dict = db.get('Products', {})
        product = products_dict.get(product_id)
        if product:
            current_qty = product.get_qty()
            # Update the product quantity by adding the input quantity.
            product.set_qty(int(current_qty) + int(inventory_form.quantity.data))
            

            stock_dict = db.get('Stock', {})
            for a_stock_id in stock_dict:
                stock = stock_dict.get(stock_id)
                if not stock.get_confirmed_status():
                    stock.confirmed()  # mark this stock entry as confirmed
            
            db['Products'] = products_dict
            db['Stock'] = stock_dict
            db.close()
            flash(f'Inventory for {product.get_name()} updated!', 'success')
        else:
            db.close()
            flash('Product not found', 'danger')
    else:
        flash("Form validation error", "danger")
    return redirect(url_for('view_stock'))

@app.route('/update-product/<int:id>/', methods=['POST', 'GET'])
def update_product(id):
    update_product = ProductForm(request.form)
    # create object of ProductForm class
    if request.method == 'POST' and update_product.validate(): # if update is valid
        products_dict = {}
        db = shelve.open('storage.db', 'w')
        products_dict = db['Products']
        product = products_dict.get(id)
        product.set_name(update_product.name.data)
        product.set_description(update_product.description.data)
        product.set_qty(update_product.qty.data)
        product.set_selling_price(update_product.selling_price.data)
        product.set_cost_price(update_product.cost_price.data)
        product.set_visible(update_product.visible.data)
        product.set_category(update_product.category.data)
        action = request.form.get('action')
        if action == 'Submit': 
            for uploaded_image in request.files.getlist('images'):
                if uploaded_image.filename == '': # if no image uploaded
                    break
                else:
                    saved_image = Image.save_image(uploaded_image)
                    image_path = f"images/{saved_image}"
                    image_dict = {}
                    try:
                        image_dict = db['Images']
                        old_image_id = db['ImageIDs']
                        new_image_id = old_image_id + 2
                    except:
                        print("Error in retrieving Image from image.db")
                        db['ImageIDs'] = 40
                        new_image_id = db['ImageIDs'] + 2
                    image_dict[new_image_id] = image_path
                    db['Images'] = image_dict
                    db['ImageIDs'] = new_image_id
                    product.add_image_id(new_image_id)
                    product.check_default_image()

            products_dict[id] = product
            db['Products'] = products_dict
            db.close()
            flash(f'Product {update_product.name.data} updated!', 'success')
            return redirect(url_for('product_management'))
        if action == 'generate':
            if update_product.description.data:
                response = generate_response(update_product.description.data, update_product.name.data)
                update_product.description.data = response
                flash('Description generated successfully!', 'success')
            else:
                flash('Please enter a description before generating!', 'danger')
            return render_template('update-product.html', form=update_product, title = "Update Product", product = product)
        
    
    
    else: # for the get request - preload the page with existing details
          # idk why but theres type error if i dont fill it?
        products_dict = {}
        db = shelve.open('storage.db', 'r')
        try:
            products_dict = db['Products']
        except:
            print("Error in retrieving Products from storage.db")
        db.close()
        
        # populate form with existing data
        product = products_dict.get(id)
            
        update_product.name.data = product.get_name()
        update_product.description.data = product.get_description()
        update_product.qty.data = product.get_qty()
        update_product.selling_price.data = product.get_selling_price()
        update_product.cost_price.data = product.get_cost_price()
        update_product.visible.data = product.get_visible()
        update_product.category.data = product.get_category()
        print(product)
        return render_template('update-product.html', form=update_product,
                               title = "Update Product", product = product)

@app.route('/delete-image/<int:product_id>/<int:image_id>', methods=['POST', 'GET'])
def delete_image(product_id, image_id):
    db = shelve.open('storage.db', 'w')
    try:
        images_dict = db['Images']
        products_dict = db['Products']
    except:
        print("Error in retrieving Images from storage.db")
    product = products_dict.get(product_id)
    list_of_image_id = product.get_images_id()
    if image_id in images_dict and image_id != 1:
        Image.delete_image(images_dict[image_id])
        images_dict.pop(image_id)
        product.remove_image_id(image_id)
    elif image_id ==1 and len(list_of_image_id) == 1:
        flash("Add another image before deleting the default image", 'danger')
    product.check_default_image()
    products_dict[product_id] = product
    db['Products'] = products_dict

        

    return redirect(url_for('update_product', id=product_id)) # reroute to update product page


@app.route('/delete-product/<int:id>', methods=['POST'])
def delete_product(id):
    # stored variable id is passed from delete button @ product-management
    products_dict = {}
    db = shelve.open('storage.db', 'w')
    products_dict = db['Products']
    product = products_dict.get(id)
    for image_id in product.get_all_images():
        remove_filepath = image_id.split('/')[1]
        Image.delete_image(remove_filepath)
    products_dict.pop(id)
    
    
    db['Products'] = products_dict
    db.close()
    flash(f'Product deleted!', 'success')
    return redirect(url_for('product_management'))

@app.route('/view-product/<int:id>', methods=['GET', 'POST'])
def view_product(id):
    products_dict = {}
    reviews_dict = {}
    db = shelve.open('storage.db', 'c')
    try:
        products_dict = db['Products']
        reviews_dict = db['Reviews']
        image_dict = db['Images']
    except:
        db['Reviews'] = {}
        reviews_dict = db['Reviews']
    db.close()
    products_list = []
    for key in products_dict:
        product = products_dict.get(id)
        all_product = products_dict.get(key)
        products_list.append(all_product)

    random.shuffle(products_list)
    
    review_list = []
    for review in reviews_dict.values():
        if review.get_product_id() == id:
            review_list.append(review)
    review_form = ReviewForm()
    if request.method == 'POST' and 'rating' in request.form:
        try:
            author = session.get('username', "Anonymous")
            rating = review_form.rating.data
            comment = review_form.comment.data.strip()
            date = datetime.today().strftime('%Y-%m-%d')
            
            # Open database in write mode
            with shelve.open('storage.db', writeback=True) as db:
                # Get or create reviews collection
                reviews_dict = db.setdefault('Reviews', {})
                review_id = db.get('ReviewIDs', 0)
                
                # Create and store new review
                new_review = Review(author, rating, comment, id, date)
                print(new_review)
                reviews_dict[new_review.get_review_id()] = new_review
                
                # Update review ID counter
                db['ReviewIDs'] = review_id + 1
                db.sync()
            
                
            flash('Review submitted successfully!', 'success')
            return redirect(url_for('view_product', id=id))

        except Exception as e:
            print(f"Error submitting review: {str(e)}")
            flash('Error submitting review. Please try again.', 'danger')
            return redirect(url_for('view_product', id=id))
    if request.method == 'POST' and request.form.get('product_name'):
        product_name = request.form.get('product_name')
        unit_price = float(request.form.get('unit_price', 0))
        try:
            quantity = 1
            with shelve.open('storage.db', writeback=True) as db:
                if 'cart' not in db:
                     db['cart'] = {'items': []}

                cart_items = db['cart']['items']

                for item in cart_items:
                    if item['name'] == product_name:
                        item['quantity'] += quantity
                        item['total_price'] = item['unit_price'] * item['quantity']
                        break
                else:
                    cart_items.append({
                        'name': product_name,
                        'unit_price': unit_price,
                        'quantity': quantity,
                        'total_price': unit_price * quantity
                    })

                db['cart']['items'] = cart_items
            flash(f"{product_name} successfully added to cart!", 'success')
        except Exception as e:
            flash(f"Error adding product to cart: {e}", 'danger')
    return render_template('view-product.html', product=product, title = "View Product",
                           review_form=review_form, review_list=review_list, products_list=products_list[:5])
    


@app.route('/fwfinfo')
def food_waste_friday():
    return render_template('fwfinfo.html')

@app.route('/foodcollectionprograminfo')
def program():
    return render_template('foodcollectionprograminfo.html')

@app.route('/user_fwf', methods=['GET', 'POST'])
def fwf_user():
    fwf_user_form = UserFWF(request.form)
    if request.method == 'POST' and fwf_user_form.validate():
        fwfuser_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            fwfuser_dict = db['FWFUser']
            fwfuser_id = db['FWFUserIDs']
            FWFUser.count_id= fwfuser_id

        except:
            print("Error in retrieving data from FWFUser.db")
        fwfUser = FWFUser(fwf_user_form.first_name.data, fwf_user_form.last_name.data,
                                  fwf_user_form.gender.data, fwf_user_form.email.data, fwf_user_form.remarks.data or '')
        fwfuser_dict[fwfUser.get_fwfuser_id()] = fwfUser
        db['FWFUser'] = fwfuser_dict
        db['FWFUserIDs'] = FWFUser.count_id
        db.close()

        return redirect(url_for('view', fwfuser_id=fwfUser.get_fwfuser_id()))

    return render_template('user_fwf.html', form=fwf_user_form)


@app.route('/regconfirm/<int:fwfuser_id>', methods=['GET'])
def view(fwfuser_id):
    try:
        db = shelve.open('storage.db', 'r')
    except:
        print("Error in retrieving data from storage.db")
        db = shelve.open('storage.db', 'c')
        db['FWFUser'] = {}
    try:
        fwfuser_dict = db['FWFUser']

        fwfuser = fwfuser_dict.get(fwfuser_id)

        if fwfuser:
            return render_template('regconfirm.html', fwfuser=fwfuser)
        else:
            return f"FWFuser with ID {fwfuser_id} not found."

    except KeyError:
        return "Error: User data not found in the database."

    except Exception as e:
        # Handle any unexpected errors
        print(f"Error retrieving user: {str(e)}")
        return "An error occurred while retrieving the user."

    finally:
        db.close()

@app.route('/Editfwfuser/<int:id>/', methods=['GET', 'POST'])
def edit_fwfuser(id):
    edit_fwfuser_form = UserFWF(request.form)

    if request.method == 'POST' and edit_fwfuser_form.validate():
        db = shelve.open('storage.db', 'w')
        fwfuser_dict = db.get('FWFUser', {})

        fwfuser = fwfuser_dict.get(id)

        if fwfuser:
            fwfuser.set_first_name(edit_fwfuser_form.first_name.data)
            fwfuser.set_last_name(edit_fwfuser_form.last_name.data)
            fwfuser.set_gender(edit_fwfuser_form.gender.data)
            fwfuser.set_email(edit_fwfuser_form.email.data)
            fwfuser.set_remarks(edit_fwfuser_form.remarks.data)

            db['FWFUser'] = fwfuser_dict

        db.close()

        # Redirect to a confirmation or another page after the update
        return redirect(url_for('fwfuser_ADretrieve', fwfuser_id=fwfuser.get_fwfuser_id()))

    else:
        # Open the shelve database in read mode
        try:
            db = shelve.open('storage.db', 'r')
        except:
            print("Error in retrieving data from storage.db")
            db = shelve.open('storage.db', 'c')
            db['FWFUser'] = {}

        # Retrieve the users' data
        fwfuser_dict = db.get('FWFUser', {})
        db.close()

        # Get the user data using the ID from the URL
        fwfuser = fwfuser_dict.get(id)

        if fwfuser:
            # Populate the form with the current user data
            edit_fwfuser_form.first_name.data = fwfuser.get_first_name()
            edit_fwfuser_form.last_name.data = fwfuser.get_last_name()
            edit_fwfuser_form.gender.data = fwfuser.get_gender()
            edit_fwfuser_form.email.data = fwfuser.get_email()
            edit_fwfuser_form.remarks.data = fwfuser.get_remarks()

        # Pass both the form and the user data to the template
        return render_template('Editfwfuser.html', form=edit_fwfuser_form, fwfuser=fwfuser)
        return redirect(url_for('fwfuser_ADretrieve'))

@app.route('/delete_fwfuser/<int:id>/', methods=['POST'])
def delete_fwfuser(id):
    db = shelve.open('FWFUser.db', 'w')

    # Retrieve the users' data from the database
    fwfuser_dict = db.get('FWFUser', {})


    if id in fwfuser_dict:
        del fwfuser_dict[id]
        db['FWFUser'] = fwfuser_dict

    db.close()

    return redirect(url_for('fwfuser_ADretrieve'))


@app.route('/fwfuser_ADretrieve', methods=['GET'])
def fwfuser_ADretrieve():
    fwfusers_dict ={}
    try:
        db = shelve.open('storage.db', 'r')
    except:
        print("Error in retrieving data from storage.db")
        db = shelve.open('storage.db', 'c')
        db['FWFUser'] = {}

    fwfusers_dict = db['FWFUser']
    db.close()
    fwfusers_list = []
    for key in fwfusers_dict:
        fwfuser = fwfusers_dict.get(key)
        fwfusers_list.append(fwfuser)

    return render_template('fwfuser_ADretrieve.html', count=len(fwfusers_list), fwfusers_list=fwfusers_list)


@app.route('/collectformR')
def message():
    return render_template('collectformR.html')

@app.route('/collectfood', methods=['GET', 'POST'])
def collect_food():
    cf_form= CollectFood(request.form)
    if request.method == 'POST' and cf_form.validate():
        collect_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            collect_dict = db['Collectusers']
            collect_id = db['CollectusersIDs']
            Collect.count_id= collect_id

        except:
            print("Error in retrieving data.")
        CollectUser = Collect(cf_form.name.data, cf_form.email.data,
                                  cf_form.type.data,cf_form.method.data, cf_form.address.data, cf_form.time.data )
        collect_dict[CollectUser.get_collect_id()] = CollectUser
        db['Collectusers'] = collect_dict
        db['CollectusersIDs'] = Collect.count_id
        db.close()

        return redirect(url_for('message'))

    return render_template('collectfood.html', form=cf_form)

@app.route('/Rcollect_Admin', methods=['GET'])
def Ad_collect():
    Admincollect_dict ={}
    try:
        db = shelve.open('storage.db', 'r')
    except:
        print("Error in retrieving data from storage.db")
        db = shelve.open('storage.db', 'c')
        db['Collectusers'] = {}

    Admincollect_dict = db['Collectusers']
    db.close()
    partners_list = []
    for key in Admincollect_dict:
        partner = Admincollect_dict.get(key)
        partners_list.append(partner)

    return render_template('Rcollect_Admin.html', count=len(partners_list), partners_list=partners_list)



@app.route('/Editpartner/<int:id>/', methods=['GET', 'POST'])
def edit_partner(id):
    edit_partner_form = CollectFood(request.form)

    if request.method == 'POST' and edit_partner_form.validate():
        # Open shelve in write mode
        db = shelve.open('storage.db', 'w')
        partner_dict = db.get('Collectusers', {})

        partner = partner_dict.get(id)

        if partner:
            partner.set_name(edit_partner_form.name.data)
            partner.set_email(edit_partner_form.email.data)
            partner.set_type(edit_partner_form.type.data)
            partner.set_method(edit_partner_form.method.data)
            partner.set_address(edit_partner_form.address.data)
            partner.set_time(edit_partner_form.time.data)

            # Save updated data
            db['Collectusers'] = partner_dict

        db.close()

        # Redirect to admin page after successful update
        return redirect(url_for('Ad_collect'))

    else:
        # Open shelve in read mode
        db = shelve.open('storage.db', 'r')
        partner_dict = db.get('Collectusers', {})
        db.close()

        # Retrieve the partner by ID
        partner = partner_dict.get(id)

        if not partner:
            # Handle case where partner is not found
            return "Partner not found", 404

        # Populate the form with partner data
        edit_partner_form.name.data = partner.get_name()
        edit_partner_form.email.data = partner.get_email()
        edit_partner_form.type.data = partner.get_type()
        edit_partner_form.method.data = partner.get_method()
        edit_partner_form.address.data = partner.get_address()
        edit_partner_form.time.data = partner.get_time()

    # Render the edit form
    return render_template('Editpartner.html', form=edit_partner_form, partner=partner)

@app.route('/approve_partner/<int:id>')
def approve_partner(id):
    db = shelve.open('storage.db', 'w')
    partner_dict = db.get('Collectusers', {})
    approved_dict = db.get('Approvedusers', {})

    partner = partner_dict.pop(id, None)  # Remove from pending
    if partner:
        approved_dict[id] = partner  # Add to approved

    db['Collectusers'] = partner_dict
    db['Approvedusers'] = approved_dict
    db.close()

    return redirect(url_for('Ad_collect'))

@app.route('/reject_partner/<int:id>')
def reject_partner(id):
    db = shelve.open('storage.db', 'w')
    partner_dict = db.get('Collectusers', {})
    rejected_dict = db.get('Rejectedusers', {})

    partner = partner_dict.pop(id, None)  # Remove from pending
    if partner:
        rejected_dict[id] = partner  # Add to rejected

    db['Collectusers'] = partner_dict
    db['Rejectedusers'] = rejected_dict
    db.close()

    return redirect(url_for('Ad_collect'))


@app.route('/ApproveCollect', methods=['GET'])
def approved_partners():
    approved_dict = {}
    try:
        # Open the shelve database in read mode
        db = shelve.open('storage.db', 'r')
        approved_dict = db.get('Approvedusers', {})  # Retrieve only approved users
    except Exception as e:
        print(f"Error in retrieving data from storage.db: {e}")
        approved_dict = {}  # Default to empty if any error occurs
    finally:
        db.close()

    partners_list = []
    for key, partner in approved_dict.items():
        partners_list.append(partner)

    # Render the Approved Partners page with the list of approved partners
    return render_template('ApproveCollect.html', count=len(partners_list), partners_list=partners_list)

def get_waste_data():
    """Retrieve stored waste data."""
    with shelve.open("storage.db") as db:
        return db.get("waste_records", {"history": [], "total_waste": 0, "total_fertilizer": 0})

def save_waste_data(data):
    """Save updated waste data."""
    with shelve.open("storage.db", writeback=True) as db:
        db["waste_records"] = data

@app.route('/N', methods=['GET', 'POST'])
def n_dashboard():
    waste_data = get_waste_data()

    # Retrieve approved partners
    db = shelve.open('storage.db', 'r')
    approved_partners = db.get('Approvedusers', {})
    db.close()

    if request.method == 'POST':
        partner_id = int(request.form.get("partner_id"))
        collected_waste = float(request.form.get("collected_waste", 0))

        # Find selected partner
        partner_name = approved_partners.get(partner_id).get_name() if partner_id in approved_partners else "Unknown"

        # Add today's waste data
        today_date = datetime.now().date()
        waste_entry = {
            "date": str(today_date),
            "partner_id": partner_id,
            "partner_name": partner_name,
            "collected": collected_waste
        }
        waste_data["history"].append(waste_entry)

        # Update totals
        waste_data["total_waste"] += collected_waste
        new_fertilizer = collected_waste * 0.4
        waste_data["total_fertilizer"] += new_fertilizer

        save_waste_data(waste_data)
        return redirect(url_for("n_dashboard"))

    return render_template(
        "N.html",
        partners=approved_partners,
        waste_history=waste_data["history"],
        total_waste=waste_data["total_waste"],
        total_fertilizer=waste_data["total_fertilizer"]
    )

@app.route('/search-by-image', methods=['POST'])
def image_search_route():
    return search_by_image()


def run():
    if __name__ == '__main__':
        initial_settings.insert_all()
        
        app.run(debug=True)

run()
