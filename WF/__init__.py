from flask import Flask, render_template, request, flash, redirect, url_for
from forms import CheckoutForm, PaymentForm
import shelve

app = Flask(__name__)
app.secret_key = 'secret_key_for_flash_messages'  # Required for flash messages and WTForms

def get_storage():
    return shelve.open('storage', writeback=True)

@app.route('/')
def home():
    return render_template('home.html', title="Home")

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
    return render_template('join-us.html', title="Join Us")

if __name__ == '__main__':
    app.run(debug=True)
