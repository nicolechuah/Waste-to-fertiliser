from wtforms import Form, StringField, IntegerField, FloatField, BooleanField, validators
from flask_wtf.file import FileField, FileAllowed

class ProductForm(Form):
    name = StringField('Product Name', [validators.Length(min=3, max=150, message="Product name must be 3-150 characters long"), validators.DataRequired
                                        (message="Please enter a product name.")])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'],message="Only jpg, jpeg, png files are allowed.")])
    description = StringField('Product Description', [validators.Length(min=1, max=1000), validators.DataRequired
                                                      (message="Please enter a product description.")])
    qty = IntegerField('Quantity', [validators.NumberRange(min=1, max=1000), validators.DataRequired(message="Please enter a quantity.")])
    selling_price = FloatField('Selling Price', [validators.NumberRange(min=1, max=10000), validators.DataRequired(message="Please enter a selling price.")])
    cost_price = FloatField('Cost Price', [validators.NumberRange(min=1, max=10000), validators.DataRequired(message="Please enter a cost price.")])
    in_stock = BooleanField('In Stock', [validators.Optional()], default=True)
    
    