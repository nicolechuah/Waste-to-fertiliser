from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Optional

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
