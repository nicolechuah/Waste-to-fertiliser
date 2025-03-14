
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp, Optional
from wtforms import Form, StringField, IntegerField, FloatField, BooleanField, validators, SubmitField,RadioField, HiddenField
from wtforms import PasswordField, BooleanField, TextAreaField, SelectField, EmailField, SelectMultipleField, widgets
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
    
    
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

categories = [("All", "All"),("Fertiliser", "Fertiliser"),("Seeds", "Seeds"),
              ("Tools", "Gardening Tools"),("Pots", "Pots & Planters")]

class ProductForm(Form):
    name = StringField('Product Name', [validators.Length(min=3, max=50, message="Product name must be 3-150 characters long"), validators.DataRequired
                                        (message="Please enter a product name.")])
    images = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'],message="Only jpg, jpeg, png files are allowed.")])
    description = TextAreaField('Product Description', [validators.Length(min=1, max=100000), validators.DataRequired
                                                      (message="Please enter a product description.")])
    qty = IntegerField('Quantity', [validators.NumberRange(min=0, max=1000000), validators.DataRequired(message="Please enter a quantity.")])
    selling_price = FloatField('Selling Price', [validators.NumberRange(min=0.5, max=10000, message="Please enter a valid number"), validators.DataRequired(message="Please enter a selling price.")])
    cost_price = FloatField('Cost Price', [validators.NumberRange(min=0.5, max=10000), validators.DataRequired(message="Please enter a cost price.")])
    visible = BooleanField('Visible', [validators.Optional()], default=True)
    category = MultiCheckboxField('Category', [validators.Optional()],choices=categories)
    

class InventoryForm(Form):
    quantity = HiddenField('Quantity', validators=[DataRequired()])
    product_id = HiddenField('Product ID', validators=[DataRequired()])

class ReviewForm(FlaskForm):
    rating = HiddenField('Rating', [validators.DataRequired()])
    comment = TextAreaField('Comment', [validators.Length(min=1, max=500), validators.optional()])

class UserFWF(Form):
    first_name = StringField('First Name', [
            validators.Length(min=1, max=150, message="First name must be between 1 and 150 characters."),
            validators.DataRequired(message="First name is required."),
            Regexp(r"^[a-zA-Z\s'-]+$", message="First name can only contain letters, spaces, hyphens, and apostrophes.")])
    
    last_name = StringField('Last Name', [validators.Length(min=1, max=150, message="Last name must be between 1 and 150 characters."),
    validators.DataRequired(message="Last name is required."),Regexp(r"^[a-zA-Z\s'-]+$", message="Last name can only contain letters, spaces, hyphens, and apostrophes.")])

    gender = SelectField('Gender', [validators.DataRequired(message="Please select a gender.")], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male'),('U', 'Unknown')])
    
    email = EmailField('Email Address', [validators.Length(min=6, max=120, message="Email must be between 6 and 120 characters."),validators.DataRequired(message="Email is required."),
        validators.Email(message="Please enter a valid email address.")])
    
    remarks = TextAreaField('Remarks', [validators.Optional()])

class CheckoutForm(FlaskForm):
    full_name = StringField('Full Name', validators=[
        DataRequired(message="Full Name is required."),
        Length(min=3, message="Full Name must be at least 3 characters.")
    ])
    phone_number = StringField('Phone Number', validators=[
        DataRequired(message="Phone Number is required."),
        Regexp(r'^\d+$', message="Phone Number must contain only digits.")
    ])
    postal_code = StringField('Postal Code', validators=[
        DataRequired(message="Postal Code is required."),
        Regexp(r'^\d+$', message="Postal Code must contain only digits.")
    ])
    address = StringField('Address', validators=[
        DataRequired(message="Address is required.")
    ])
    unit_number = StringField('Unit Number', validators=[
        Optional(),
        Regexp(r'^\d*$', message="Unit Number must contain only digits.")
    ])
    submit = SubmitField('Proceed to Payment')

class PaymentForm(FlaskForm):
    cardholder_name = StringField('Cardholder Name', validators=[
        DataRequired(message="Cardholder Name is required."),
        Length(min=2, message="Cardholder Name must be more than 1 character.")
    ])
    card_number = StringField('Card Number', validators=[
        DataRequired(message="Card Number is required."),
        Regexp(r'^\d+$', message="Card Number must contain only digits.")
    ])
    expiry_date = StringField('Expiry Date (MM/YY)', validators=[
        DataRequired(message="Expiry Date is required."),
        Regexp(r'^\d{2}/\d{2}$', message="Expiry Date must be in the format MM/YY and contain only digits.")
    ])
    cvv = StringField('CVV', validators=[
        DataRequired(message="CVV is required."),
        Regexp(r'^\d{3}$', message="CVV must be exactly 3 digits.")
    ])
    submit = SubmitField('Submit Payment')


class CollectFood(Form):
    name = StringField('Business Name or Individual Name', [validators.Length(min=1, max=150), validators.DataRequired(),Regexp(r"^[a-zA-Z\s'-]+$", message="Name can only contain letters, spaces, hyphens, and apostrophes.")])
    email = EmailField('Email Address',
                       [validators.Length(min=6, max=120), validators.DataRequired(), validators.Email()])
    method= SelectField('Preferred Collection Method', [validators.DataRequired()],
                         choices=[('', 'Select'), ('Schedule', 'Scheduled Pick up'),('On-Demand','On-Demand Pick up'),('Drop off','Drop off Pick up')],
                         default='')
    type = RadioField('Food Waste Type', choices=[('Leftover', 'Leftover food'), ('Expired', 'Expired food'), ('Spoiled', 'Spoiled or Damaged food'), ('Others','Others')],
                            default='', validators=[validators.DataRequired()])
    address =StringField('Location Address',[validators.length(min=1, max=250), validators.DataRequired(message='Please fill your address')])
    time = SelectField('Preferred Time slot', [validators.DataRequired()],
                         choices=[('', 'Select'), ('Morning', 'Morning 8AM-11AM'),('Afternoon','Afternoon 1PM-4PM'),('Evening','Evening 5PM-8PM')],
                         default='')
    
class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')