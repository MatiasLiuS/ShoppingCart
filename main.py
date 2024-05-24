'''
To reset the database, run this command in the Shell: 
  sqlite3 myDatabase.db ".read create.sql"
'''
import sqlite3 
import datetime
import uuid

from flask import Flask, render_template, request, session, redirect, url_for


# ---------------------------------------------Set Connection---------------------------------------------#
app = Flask('app')
connection = sqlite3.connect('myDatabase.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
app.secret_key = "SecretKey"
app.config["SESSION_PERMANENT"] = False
# ---------------------------------------------Set Connection---------------------------------------------#

# ---------------------------------------------Start of Normal Functions---------------------------------------------#

#-------Get the product name from the id-------#
def get_product_name(product_id):
    connection = sqlite3.connect('myDatabase.db')
    cursor = connection.cursor()
    cursor.execute("SELECT p_name FROM product WHERE p_id = ?", (product_id, ))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

#-------Get all product info from the id-------# 
def get_product_by_id(product_id):
    connection = sqlite3.connect('myDatabase.db')
    cursor = connection.cursor()

    # query the database to get the product details for the given product_id
    cursor.execute("SELECT *, p_price AS price FROM product WHERE p_id = ?", (product_id,))
    result = cursor.fetchone()
    connection.close()
    return dict(zip(['p_id', 'p_name', 'p_price', 'p_desc', 'p_inventory', 'category', 'p_image'], result)) if result else None
  
#-------Get the total price for all items-------#
def get_total_price():
  total_price = 0
  for product_id, quantity in session['cart'].items():
    product = get_product_by_id(product_id)
    total_price += product.p_price * quantity
  return total_price

#-------Get the price of an item from product id-------#
def get_product_price(product_id):
    connection = sqlite3.connect('myDatabase.db')
    cursor = connection.cursor()
    # query the database to get the price for the given product_id
    cursor.execute("SELECT p_price FROM product WHERE p_id = ?",
                   (product_id, ))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

#-------Get the inventory of an item from product id-------#
def get_product_inventory(product_id):
    connection = sqlite3.connect('myDatabase.db')
    cursor = connection.cursor()
    # query the database to get the inventory for the given product_id
    cursor.execute("SELECT p_inventory FROM product WHERE p_id = ?",
                   (product_id, ))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None

#-------Get the subtotal from all items-------#
def calculate_subtotal(cart):
    subtotal = 0
    for product_id, quantity in cart.items():
        price = get_product_price(product_id)
        subtotal += price * quantity
    return subtotal

#-------Get the tax of the subtotal-------#
def calculate_tax(subtotal, tax_rate=0.065):
    """Calculate tax based on subtotal and tax rate"""
    return subtotal * tax_rate

#-------Add the tax to the subtotal and get overall total-------#
def calculate_total(subtotal, tax):
    """Calculate total cost based on subtotal and tax"""
    return subtotal + tax

# ---------------------------------------------End of Normal Functions---------------------------------------------#

# ---------------------------------------------Start of App Routes---------------------------------------------#

#----------------------------START Home Page App Route----------------------------#
@app.route('/', methods=['GET', 'POST'])
def index():
    connection = sqlite3.connect('myDatabase.db')  #connection
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM CATEGORIES")  #DB info
    categories = cursor.fetchall()
    return render_template("home.html", categories=categories)
#----------------------------END Home Page App Route----------------------------#
  
#----------------------------START All Products App Route----------------------------#
@app.route('/collections/all')
def collections():
    connection = sqlite3.connect('myDatabase.db')  #connection
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM PRODUCT INNER JOIN CATEGORIES ON product.category = categories.c_name"
    )  #DB info
    products = cursor.fetchall()
    return render_template("all_products.html", products=products)
#----------------------------END All Products App Route----------------------------#

#----------------------------START Specific Category App Route----------------------------#
@app.route('/collections/<c_name>')
def category_type(c_name):
    connection = sqlite3.connect('myDatabase.db')  # Connection
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM PRODUCT INNER JOIN CATEGORIES ON product.category = categories.c_name WHERE categories.c_name = ?",
        (c_name, ))
    products = cursor.fetchall()
    connection.close()
    return render_template("category.html", products=products, c_name=c_name)
#----------------------------END Specific Category App Route----------------------------#
  
#----------------------------START Specific Product App Route----------------------------#
@app.route('/product/<p_id>')
def product_type(p_id):
    connection = sqlite3.connect('myDatabase.db')  # Connection
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM PRODUCT WHERE product.p_id = ?", (p_id, ))
    producto = cursor.fetchall()
    print(producto)
    connection.close()
    return render_template("product.html", producto=producto)
#----------------------------END Specific Product App Route----------------------------#

#----------------------------START Search Product App Route----------------------------#
@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search')
    connection = sqlite3.connect('myDatabase.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    query = "SELECT * FROM PRODUCT WHERE p_id LIKE ? OR p_name = ? OR category LIKE ?"
    cursor.execute(query, ('%' + search_query + '%', search_query, search_query,))
    producto = cursor.fetchall()
    connection.close()
    return render_template('search_results.html',
                           producto=producto,
                           search_query=search_query)
#----------------------------END Specific Product App Route----------------------------#

#----------------------------START Add Product to Cart----------------------------# 
@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
   #----------p_id and quantity from form ----------#
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity'))

    inventory = get_product_inventory(product_id)
  
   #----------check if cart is in session, if not create a cart----------#  
    if 'cart' not in session: 
        session['cart'] = dict()
  
   #---------add the items to cart----------#  

    #----------if the item is in the cart already, then add the quantity to the existing quantity----------# 
    if product_id in session['cart']:
        current_quantity = session['cart'][product_id]
        total_quantity = current_quantity + quantity
         #------error message if quantity is more than the stock given------# 
        if total_quantity > inventory:
           print("there are not enough items in stock. Maximum quantity for this item is {inventory - current_quantity}.")

         #------set total quantity to the product------# 
        else:  
          bob = session['cart']
          bob[product_id] += int(quantity)
          session['cart'] = bob
          print('Item(s) added to cart', 'success')
          
    #---------item is not in cart, create new key-value pair----------# 
    else:
          bob = session['cart']
          bob[product_id] = int(quantity)
          session['cart'] = bob
          print('Item added to cart', 'success')
      
    #----------debugging message ----------#
    print(f"Added {quantity} of product {product_id} to cart")
    print("Current cart contents:")
    for item, quantity in session['cart'].items():
      print(f"{item}: {quantity}")

      ##----------redirect the user back to the shopping cart page----------#
    return redirect(url_for('cart'))
#----------------------------END Add Product to Cart----------------------------#

#----------------------------START Log In App Route----------------------------#
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the form data
        username = request.form['username']
        password = request.form['password']

        connection = sqlite3.connect('myDatabase.db')  #connection
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Query the database to check if the user exists and the password is correct
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (
            username,
            password,
        ))

        user = cursor.fetchone()

        if (user is None):
            error_message = "Invalid username or password. Please try again."
            return render_template('account.html', error_message=error_message)

        else:
            print("Session variable is set.")
            
            session['username'] = user[0]
            return redirect('/')

    return render_template('account.html')

  
#----------------------------END Log In App Route----------------------------#

#----------------------------START Register App Route----------------------------#
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the form data
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        connection = sqlite3.connect('myDatabase.db')  #connection
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Check if the username is already taken
        query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            err_message = "Username already taken. Please choose a different one."
            return render_template('account.html', err_message=err_message)

        # Add the user to the database
        query = "INSERT INTO users (name, username, password) VALUES (?, ?, ?)"
        cursor.execute(query, (name, username, password))
        connection.commit()

        # Log in the user
        session['username'] = username

        
        
        return redirect('/')

    return render_template('account.html')
#----------------------------START Log Out App Route----------------------------#
@app.route('/logout')
def logout(): 
	session.clear()
	return redirect('/')
#----------------------------END Log Out App Route----------------------------#
  
# ---------------------------------------------END of App Routes---------------------------------------------#

# ---------------------------------------------Start of CART App Routes---------------------------------------------#

#----------------------------Start Cart App Route----------------------------#
@app.route('/cart', methods=['GET', 'POST'])
def cart(): 
    print("cart is being loaded")
  
    if 'cart' not in session: 
        session['cart'] = dict()
      
    subtotal = 0
    #----------Debug Cart Update----------#
    print("Current cart contents @ beginning of cart:")
    for item in session['cart']:
        print(f"{item}: {session['cart'][item]}")

    #----------Get Cart info to HTML----------#
    cart_items = {}
    for product_id, quantity in session['cart'].items():
        product = get_product_by_id(product_id)
        if product is not None:
            product['quantity'] = quantity
            product['total'] = quantity * product['p_price']
            subtotal += product['total']
            cart_items[product_id] = product
    
    tax = subtotal * 0.065
    total = subtotal + tax

    #------Request Methods (Empty Cart or Remove Item)------# 
    if request.method == 'POST':
        action = request.form.get('action')
        #----------Empty Cart----------# 
        if action == 'empty_cart':
            session.pop('cart', None)
            session['cart'] = dict()
            print('cart cleared')
            subtotal = 0
            for item in session['cart'].values():
                subtotal += item['price'] * item['quantity']
            tax = subtotal * 0.065 # Assuming tax is .065%
            total = subtotal + tax
            # Update session variables
            session['subtotal'] = subtotal
            session['tax'] = tax
            session['total'] = total
    #----------Debug Cart Update----------#
    cart_items = {}
    for product_id, quantity in session['cart'].items():
        product = get_product_by_id(product_id)
        if product is not None:
            product['quantity'] = quantity
            product['total'] = quantity * product['p_price']
            subtotal += product['total']
            cart_items[product_id] = product
    
    tax = subtotal * 0.065
    total = subtotal + tax
  
    print("Current cart contents @ end:")
    for item in session['cart']:
        print(f"{item}: {session['cart'][item]}")
      
    return render_template('cart.html', cart_items=cart_items, subtotal=subtotal, tax=tax, total=total, get_product_by_id =get_product_by_id )

#----------------------------END Cart App Route----------------------------#

#----------------------------START Item Quantity Update Route----------------------------#
@app.route('/update-quantity', methods=['POST'])
def update_quantity():
 #----------p_id and quantity from form ----------#
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity'))

  #----------if quantity is 0, then pop the item ----------#
    if quantity == 0:
        session['cart'].pop(product_id, None)

  #----------use bob to update specific items quantity ----------#
    bob = session['cart']
    bob[product_id] = int(quantity)
    session['cart'] = bob

   #----------debugging message ----------#
    print('Item updated in cart', 'success')
    print(f"Updated to {quantity} of product {product_id} to cart")
    print("Current cart contents:")
    for item, quantity in session['cart'].items():
      print(f"{item}: {quantity}")

  
    ##----------redirect the user back to the shopping cart page----------#
    print(f"refreshing cart")
    return redirect(url_for('cart', refresh=True))
#----------------------------END Item Quantity Update Route----------------------------#

#----------------------------START Remove Item Route----------------------------#
@app.route('/remove', methods=['POST'])
def remove():
    product_id = request.form['product_id']
    cart = session['cart']
    cart.pop(product_id)
    session['cart'] = cart
    return redirect(url_for('cart'))
#----------------------------END Remove Item Route----------------------------#

#----------------------------START Checkout Item Route----------------------------#
@app.route('/checkout')
def checkout():
    connection = sqlite3.connect('myDatabase.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if 'cart' not in session or len(session['cart']) == 0:
        print("couldn't check out")
        return redirect(url_for('cart'))

    # Get the total cost of the order
    total_cost = 0
    cart_items = session.get('cart', {})
    for item_id, quantity in cart_items.items():
        cursor.execute("SELECT * FROM product WHERE p_id = (?)", (item_id,))
        product = cursor.fetchone()
        total_cost += product['p_price'] * quantity

    # Insert a new row into the order_history table
    o_id = uuid.uuid4().hex # generate a unique ID for the order
    uname = session['username']
    o_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO order_history (o_id, uname, o_date, total_cost) VALUES (?, ?, ?, ?)",
                   (o_id, uname, o_date, total_cost))

    # Insert a new row into the orderItem table for each item in the cart
    for item_id, quantity in cart_items.items():
        cursor.execute("INSERT INTO orderItem (ord_id, prod_id, quantity, usr_name, ord_date) VALUES (?, ?, ?, ?, ?)",
               (o_id, item_id, quantity, uname, o_date))

        # Update the product inventory
        cursor.execute("UPDATE product SET p_inventory = p_inventory - ? WHERE p_id = ?", (quantity, item_id))

    connection.commit()
    session.pop('cart', None)
    print('cart cleared')

    return render_template('checkout.html')


#----------------------------END Checkout Item Route----------------------------#

@app.route('/orders')
def orders():
    connection = sqlite3.connect('myDatabase.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Retrieve the user's order history from the order_history table
    uname = session['username']
    cursor.execute("SELECT * FROM order_history WHERE uname = ?", (uname,))
    orders = cursor.fetchall()

    return render_template('orders.html', orders=orders)
  
app.run(host='0.0.0.0', port=8080)
