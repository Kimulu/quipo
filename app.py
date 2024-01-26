from flask import Flask, render_template, redirect, url_for, flash, request, session, make_response,jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from model import db, Product, init_db, User, Order
from forms import RegistrationForm, LoginForm 
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '0b522291d9c50d337d4bf51025d8aa0c' 
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load user callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)

        # Check if the username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'danger')
            return redirect(url_for('register'))

        # Create a new user
        user = User(username=form.username.data, password=hashed_password)

        try:
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully. You can now log in.', 'success')
            return redirect(url_for('login'))

        except IntegrityError:
            # Handle the case where the username is taken in the short time between checking and committing
            db.session.rollback()
            flash('Username already taken. Please choose a different username.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)

    
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
            
        else:
            flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html', form=form)

#logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))
    

@app.route('/dashboard')
@login_required
def dashboard():
    # Assuming current_user is the authenticated user
    user_orders = Order.query.filter_by(user_id=current_user.id).all()

    # Function to get product details from the product ID
    def get_product_details(product_id):
        product = Product.query.get(product_id)
        return product

    # Get product details for each order
    order_details = []
    for order in user_orders:
        product = get_product_details(order.product_id)
        if product:
            order_details.append({
                'product_name': product.name,
                'quantity': order.quantity,
                'price': product.price
                # Add more details as needed
            })

    return render_template('dashboard.html', user=current_user, user_orders=order_details)


@app.route('/')
def home():
    if request.method == 'POST':
        # Handle POST request if needed
        pass
    productz = Product.query.all()

    products = productz[0:3]
    return render_template('index.html', products=products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', type=int)

    if product_id is not None and quantity is not None:
        # Retrieve the cart from the session
        cart_str = session.get('cart', '{}')

        # Parse the JSON string to a dictionary
        cart = json.loads(cart_str)

        # Update the cart with the new item
        cart[product_id] = cart.get(product_id, 0) + quantity

        # Save the updated cart back to the session
        session['cart'] = json.dumps(cart)

        flash('Item added to the cart!', 'success')
        print(session['cart'])

    # Redirect back to the homepage or wherever you want
    return redirect(url_for('home'))


@app.route('/add_to_cart_shop', methods=['POST'])
def add_to_cart_shop():
    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', type=int)

    if product_id is not None and quantity is not None:
        # Retrieve the cart from the session
        cart_str = session.get('cart', '{}')

        # Parse the JSON string to a dictionary
        cart = json.loads(cart_str)

        # Update the cart with the new item
        cart[product_id] = cart.get(product_id, 0) + quantity

        # Save the updated cart back to the session
        session['cart'] = json.dumps(cart)

        flash('Item added to the cart!', 'success')
        print(session['cart'])

    # Redirect back to the homepage or wherever you want
    return redirect(url_for('shop'))


# New route to show the cart
@app.route('/cart', methods=['GET', 'POST'])
def show_cart():
    if request.method == 'GET':
        # Retrieve the cart from the session
        cart_str = session.get('cart', '{}')

        # Parse the JSON string to a dictionary
        cart = json.loads(cart_str)

        print("Cart from session:", cart)

        # Retrieve product details from the database based on product IDs in the cart
        products = Product.query.filter(Product.id.in_(cart.keys())).all()

        print("Product IDs from the database:", [product.id for product in products])

        # Create a dictionary to store product details with quantity
        cart_details = {
            product.id: {
                'name': product.name,
                'price': product.price,
                'quantity': cart.get(str(product.id), 0),
                'image_url': product.image_url
            } for product in products
        }

        # Calculate the total of the cart
        total = calculate_cart_total(cart_details)

        return render_template('cart.html', cart=cart_details, total=total)

    elif request.method == 'POST':
        # Your code for handling POST requests, if needed

        # Ensure to return a response, even if it's just an empty string
        return redirect(url_for('show_cart'))

@app.route('/change_quantity', methods=['POST'])
def change_quantity():
    # Retrieve the product_id and change from the form data
    product_id = request.form.get('product_id', type=int)
    change = request.form.get('change', type=int)

    if product_id is not None and change is not None:
        # Retrieve the cart from the session
        cart_str = session.get('cart', '{}')

        # Parse the JSON string to a dictionary
        cart = json.loads(cart_str)

        # Change the quantity for the specified product
        cart[str(product_id)] = max(cart.get(str(product_id), 0) + change, 0)

        # Save the updated cart back to the session
        session['cart'] = json.dumps(cart)

    return redirect(url_for('show_cart'))

# Function to calculate the total of the cart
def calculate_cart_total(cart_details):
    total = 0.0
    for details in cart_details.values():
        total += details['price'] * details['quantity']
    return total

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    # Retrieve the product_id from the form data
    product_id = request.form.get('product_id', type=int)

    if product_id is not None:
        # Retrieve the cart from the session
        cart_str = session.get('cart', '{}')

        # Parse the JSON string to a dictionary
        cart = json.loads(cart_str)

        # Remove the specified product from the cart
        if str(product_id) in cart:
            del cart[str(product_id)]

            # Save the updated cart back to the session
            session['cart'] = json.dumps(cart)

            # Return a JSON response indicating success
            return jsonify({'status': 'success'})

    # Return a JSON response indicating failure
    return jsonify({'status': 'error'})


@app.route('/cart_count')
def cart_count():
    cart_str = session.get('cart', '{}')
    cart = json.loads(cart_str)
    count = sum(cart.values())
    return jsonify({'count': count})



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/checkout')
def checkout():
     # Check if the user is authenticated
    user_authenticated = current_user.is_authenticated

    # Retrieve the cart from the session
    cart_str = session.get('cart', '{}')

    # Parse the JSON string to a dictionary
    cart = json.loads(cart_str)

    # Retrieve product details from the database based on product IDs in the cart
    products = Product.query.filter(Product.id.in_(cart.keys())).all()

    # Create a dictionary to store product details with quantity
    cart_details = {
        product.id: {
            'name': product.name,
            'price': product.price,
            'quantity': cart.get(str(product.id), 0),
            'image_url': product.image_url
        } for product in products
    }

    # Calculate the total of the cart
    total = calculate_cart_total(cart_details)

    return render_template('checkout.html', cart=cart_details, total=total,user_authenticated=user_authenticated)


# Save order route
@app.route('/save_order', methods=['POST'])
@login_required
def save_order():
    try:
        data = request.get_json()
        print(data)

        # Retrieve the current user's ID
        user_id = current_user.id

        # Save product details to the database
        for product_id, product_details in data['details']['products'].items():
            order = Order(
                order_id=data['orderID'],
                user_id=user_id,
                product_id=int(product_id),
                quantity=product_details['quantity'],
            )
            db.session.add(order)

        # Commit changes
        db.session.commit()

        # Clear the cart after processing the order
        session.pop('cart', None)

        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})



@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/shop')
def shop():
    if request.method == 'POST':
            # Handle POST request if needed
            pass
    products = Product.query.all()
    return render_template('shop.html', products=products)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_db()
    app.run(debug=True)