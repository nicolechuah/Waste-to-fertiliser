from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms import Form, StringField, IntegerField, FloatField, BooleanField, validators, SubmitField
from wtforms import PasswordField, BooleanField, TextAreaField, SelectField, EmailField
from flask_login import current_user
import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AccountForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=2, max=20)])
    email = StringField('Email', validators=[Email()])
    current_password = PasswordField('Current Password', render_kw={'readonly': True})
    password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('password')])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

class DeleteAccountForm(FlaskForm):
    submit = SubmitField('Delete Account')
    
class ProductForm(Form):
    name = StringField('Product Name', [validators.Length(min=3, max=50, message="Product name must be 3-150 characters long"), validators.DataRequired
                                        (message="Please enter a product name.")])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'],message="Only jpg, jpeg, png files are allowed.")])
    description = StringField('Product Description', [validators.Length(min=1, max=1000), validators.DataRequired
                                                      (message="Please enter a product description.")])
    qty = IntegerField('Quantity', [validators.NumberRange(min=1, max=1000), validators.DataRequired(message="Please enter a quantity.")])
    selling_price = FloatField('Selling Price', [validators.NumberRange(min=1, max=10000), validators.DataRequired(message="Please enter a selling price.")])
    cost_price = FloatField('Cost Price', [validators.NumberRange(min=1, max=10000), validators.DataRequired(message="Please enter a cost price.")])
    visible = BooleanField('Visible', [validators.Optional()], default=True)

class UserFWF(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],
                         choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')],
                         default='')
    email = EmailField('Email Address',
                       [validators.Length(min=6, max=120), validators.DataRequired(), validators.Email()])

    remarks = TextAreaField('Remarks', [validators.Optional()])
