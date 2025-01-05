from flask import Flask, render_template, request, redirect, url_for

products = [
    {
    "id": "1",
    "name": "Product 1",
    "description": "This is a description of product 1",
    "qty": "10",
    "selling_price": "100.00",
    "cost_price": "50.00",
    "in_stock": "True"
},
{
    "id": "2",
    "name": "Product 2",
    "description": "This is a description of product 2",
    "qty": "20",
    "selling_price": "200.00",
    "cost_price": "100.00",
    "in_stock": "True"
},
{
    "id": "3",
    "name": "Product 3",
    "description": "This is a description of product 3",
    "qty": "30",
    "selling_price": "300.00",
    "cost_price": "150.00",
    "in_stock": "False"
}

]


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', products=products, title = "Products")

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/join-us')
def join_us():
    return render_template('join-us.html')


if __name__ == '__main__':
    app.run(debug=True)
