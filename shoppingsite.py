"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken, Katie Byers.
"""

from flask import Flask, render_template, redirect, flash, session, request
import jinja2

import customers
import melons

app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'jqoiwjefsdf'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list, 
                           Melon=melons.Melon)


@app.route("/melon/<melon_id>")
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print(melon)
    return render_template("melon_details.html",
                           display_melon=melon, 
                           Melon=melons.Melon)


@app.route("/cart")
def show_shopping_cart():
    """Display content of shopping cart."""

    # If cart doesn't exist in session, render empty_cart page
    if 'cart' not in session:
        flash("Your cart is empty!")
        return render_template('empty_cart.html')
    
    # Initialize variables
    cart = session['cart']
    melons_in_cart = []
    total_cost = 0

    for melon_id in cart:
        # Access melon object
        melon = melons.get_by_id(melon_id)

        # Update melon.qty attribute
        melon.qty = cart[melon_id]

        # Update melon.total_price
        melon.total_price = melon.price * cart[melon_id]
        total_cost += melon.total_price

        # Add melon object to cart list
        melons_in_cart.append(melon)

    return render_template("cart.html", 
                           melons=melons_in_cart, 
                           total=total_cost, 
                           Melon=melons.Melon)


@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Melon successfully added to
    cart'."""
    
    # Create cart in session
    if 'cart' not in session:
        session['cart'] = {}
    
    # Populate melons to the user's cart with a flash msg when successful
    if melon_id not in session['cart']:
        session['cart'][melon_id] = 1
    else:
        session['cart'][melon_id] += 1
    flash("Melon successfully added to cart")

    return redirect('/cart')


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    email = request.form.get('email')
    password = request.form.get('password')
    
    user = customers.get_by_email(email)
    if user != None:
        if password == user.password:
            flash('Successfully logged in.')
            return redirect('/melons')
        flash('Incorrect username and/or password.')
        return redirect('/login')
    
    flash('Username does not exist.')
    return redirect('/login')


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
