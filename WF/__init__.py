from flask import Flask, render_template, url_for, flash, redirect, request, session
from AllForms import RegistrationForm, LoginForm, AccountForm, ProductForm, UserFWF, CheckoutForm, PaymentForm,CollectFood
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import shelve, User
from PIL import Image
from werkzeug.utils import secure_filename
import os
import secrets
from Product import Product
import shelve
from Fwfuser import FWFUser
from Collect import Collect


app = Flask(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd6691973382147ed2b8724aa19eb0720'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.secret_key = 'secret_key_for_flash_messages'  # Required for flash messages and WTForms

def get_storage():
    return shelve.open('storage', writeback=True)

@app.route('/')
def home():
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

    return render_template('home.html', products_list=products_list, title="Home")

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        unit_price = float(request.form.get('unit_price', 0))

        if product_name:
            try:
                quantity = 1
                with get_storage() as db:
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
                    db.sync()
                flash(f"{product_name} successfully added to cart!", 'success')
            except Exception as e:
                flash(f"Error adding product to cart: {e}", 'danger')

    return render_template('products.html', title="Products")

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart_items = []
    overall_price = 0

    with get_storage() as db:
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
            db.sync()

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
        with get_storage() as db:
            if 'delivery' not in db:
                db['delivery'] = {'records': []}
            db['delivery']['records'].append(delivery_data)
            db.sync()
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
        with get_storage() as db:
            if 'payment' not in db:
                db['payment'] = {'records': []}
            db['payment']['records'].append(payment_data)

            if 'complete' not in db:
                db['complete'] = {'items': []}
            db['complete']['items'].extend(db.get('cart', {}).get('items', []))
            db['cart'] = {'items': []}
            db.sync()

        flash("Payment successfully processed!", 'success')
        return redirect(url_for('home'))
    return render_template('payment.html', form=form, title="Payment")

@app.route('/user')
def user():
    with get_storage() as db:
        complete_data = db.get('complete', {}).get('items', [])
        delivery_data = db.get('delivery', {}).get('records', [])
        payment_data = db.get('payment', {}).get('records', [])

    return render_template('user.html', complete_data=complete_data, delivery_data=delivery_data, payment_data=payment_data, title="User Data")

@app.route('/edit-delivery/<int:id>', methods=['GET', 'POST'])
def edit_delivery(id):
    form = CheckoutForm()
    with get_storage() as db:
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
            db.sync()
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
    with get_storage() as db:
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
            db.sync()
            flash("Payment details updated successfully.", 'success')
            return redirect(url_for('user'))

        form.cardholder_name.data = payment_data[id]['cardholder_name']
        form.card_number.data = payment_data[id]['card_number']
        form.expiry_date.data = payment_data[id]['expiry_date']
        form.cvv.data = payment_data[id]['cvv']

    return render_template('payment.html', form=form, title="Edit Payment Details")


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
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
        
        flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route("/account", methods=['GET', 'POST'])
def account():
    form = AccountForm()
    users_dict = {}
    db = shelve.open('storage.db', 'c')
    users_dict = db['Users']

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

        # Update profile picture
        '''
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.set_profile_picture(picture_file)
            updated = True
        '''

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

@app.route("/account/delete", methods=['POST'])
def delete_account():
    db = shelve.open('storage.db', 'c')
    users_dict = db.get('Users', {})
    current_user_id = None

    # Find the logged-in user
    for user_id, user in users_dict.items():
        if user.get_username() == session['username']:
            current_user_id = user_id
            break

    if current_user_id:
        # Remove user from the database
        users_dict.pop(current_user_id, None)
        db['Users'] = users_dict
        db.close()

        # Clear the session and redirect
        session.pop('logged_in', None)
        session.pop('username', None)
        flash('Your account has been deleted.', 'info')
        return redirect(url_for('home'))

    db.close()
    flash('Account deletion failed. Please try again.', 'danger')
    return redirect(url_for('account'))
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
                          create_product.selling_price.data, create_product.cost_price.data, create_product.visible.data, saved_image)
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
        product.set_visible(update_product.visible.data)
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
        update_product.visible.data = product.get_visible()
        
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

@app.route('/view-product/<int:id>', methods=['GET'])
def view_product(id):
    products_dict = {}
    db = shelve.open('storage.db', 'r')
    products_dict = db['Products']
    db.close()
    
    product = products_dict.get(id)
    return render_template('view-product.html', product=product, title = "View Product")


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

## Helper functions ##
# SAVE IMAGE #
def save_image(image):
        random_hex = secrets.token_hex(8) #randomize filename
        f_name, f_ext = os.path.splitext(image.filename) #split filename and extension
        image_fn = random_hex + f_ext #combine random hex and extension
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_fn) #combine root path and image path
        image.save(image_path)
        print(type(image))

        return image_fn
    
    
def delete_image(image):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image)
    if os.path.exists(image_path) and image != "default_product.png":
        os.remove(image_path)

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




if __name__ == '__main__':
    app.run(debug=True)




