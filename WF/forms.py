from wtforms import Form, StringField, IntegerField, FloatField, BooleanField, validators
from flask_wtf.file import FileField, FileAllowed

class ProductForm(Form):
    name = StringField('Product Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    description = StringField('Product Description', [validators.Length(min=1, max=500), validators.DataRequired()])
    qty = IntegerField('Quantity', [validators.NumberRange(min=1, max=1000), validators.DataRequired()])
    selling_price = FloatField('Selling Price', [validators.NumberRange(min=1, max=10000), validators.DataRequired()])
    cost_price = FloatField('Cost Price', [validators.NumberRange(min=1, max=10000), validators.DataRequired()])
    in_stock = BooleanField('In Stock', [validators.Optional()], default=True)
    
    