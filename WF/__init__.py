from flask import Flask, render_template, url_for, flash, redirect, request, session
from Forms import RegistrationForm, LoginForm, AccountForm, ProductForm, UserFWF
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


app = Flask(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd6691973382147ed2b8724aa19eb0720'
app.config['UPLOAD_FOLDER'] = 'static/images'

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

    return render_template('home.html', products_list=products_list, title = "Products")


@app.route('/help')
def help():
    return render_template('help.html')

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
        product.set_name(update_product.name.data)
        product.set_description(update_product.description.data)
        product.set_qty(update_product.qty.data)
        product.set_selling_price(update_product.selling_price.data)
        product.set_cost_price(update_product.cost_price.data)
        product.set_in_stock(update_product.in_stock.data)
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
        update_product.description.data = product.get_description()
        update_product.qty.data = product.get_qty()
        update_product.selling_price.data = product.get_selling_price()
        update_product.cost_price.data = product.get_cost_price()
        update_product.in_stock.data = product.get_in_stock()
        
        return render_template('update-product.html', form=update_product,
                               title = "Update Product")
@app.route('/delete-product/<int:id>', methods=['POST'])
def delete_product(id):
    # stored variable id is passed from delete button @ product-management
    products_dict = {}
    db = shelve.open('storage.db', 'w')
    products_dict = db['Products']
    products_dict.pop(id)
    db['Products'] = products_dict
    db.close()
    return redirect(url_for('product_management'))



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



if __name__ == '__main__':
    app.run(debug=True)
