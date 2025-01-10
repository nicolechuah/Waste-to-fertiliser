from flask import Flask, render_template, url_for, flash, redirect, request, session
from Forms import RegistrationForm, LoginForm, AccountForm
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import shelve, User
from PIL import Image
from werkzeug.utils import secure_filename
import os
import secrets


app = Flask(__name__)
app.config['SECRET_KEY'] = 'd6691973382147ed2b8724aa19eb0720'
app.config['UPLOAD_FOLDER'] = 'static/images'

@app.route('/')
def home():
    return render_template('home.html', title = "Products")

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
        db = shelve.open('user.db', 'c')
        user_id = db.get('UserIDs', 0)
        user_id += 1

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

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
        db = shelve.open('user.db', 'r')
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
    db = shelve.open('user.db', 'c')
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
    db = shelve.open('user.db', 'c')
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

if __name__ == '__main__':
    app.run(debug=True)