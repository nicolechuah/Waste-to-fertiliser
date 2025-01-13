from flask import Flask, render_template, url_for, flash, redirect, request, session
from Forms import RegistrationForm, LoginForm, AccountForm, ProductForm
from flask_bcrypt import Bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import shelve, User
from PIL import Image
from werkzeug.utils import secure_filename
import os
import secrets
from Product import Product
import shelve

from flask import Flask, render_template, request, redirect, url_for,session
from Forms import UserFWF
from Fwfuser import FWFUser
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


if __name__ == '__main__':
    app.run(debug=True)
