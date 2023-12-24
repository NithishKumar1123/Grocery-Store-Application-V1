from flask import request, redirect, render_template
from flask import current_app as app
from application.database import db
from application.models import User, Category, Product, Cart

# USER

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username = username, password = password).first()
        if(user):
            link = "/" + str(user.userid) + "/read_product"
            return redirect(link)
        else:
            return render_template("not_a_user.html")
            
@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        user = User(username = username, password = password)
        db.session.add(user)
        db.session.commit()
        return render_template("user_registered.html")

@app.route("/<int:userid>/profile")
def profile(userid):
    user = User.query.filter_by(userid = userid).first()
    if(user):
        cart = Cart.query.filter_by(userid = userid).all()
        return render_template("profile.html", user = user, cart = cart)
    else:
        return render_template("not_a_user.html")

# CART
        
@app.route("/<int:userid>/update_cart/<int:productid>", methods = ["GET", "POST"])
def update_cart(userid, productid):
    if request.method == "GET":
        user = User.query.filter_by(userid = userid).first()
        if(user):
            cart = Cart.query.filter_by(userid = userid, productid = productid).first()
            return render_template("update_cart.html", user = user, cart = cart)
        else:
            return render_template("not_a_user.html")
    else:
        quantity = request.form["quantity"]
        cart = Cart.query.filter_by(userid = userid, productid = productid).first()
        cart.quantity = quantity
        db.session.commit()
        link = "/" + str(userid) + "/cart"
        return redirect(link)
        
@app.route("/<int:userid>/delete_cart/<int:cartid>")
def delete_cart(userid, cartid):
    user = User.query.filter_by(userid = userid).first()
    if(user):
        cart = Cart.query.filter_by(cartid = cartid).first()
        db.session.delete(cart)
        db.session.commit()
        link = "/" + str(userid) + "/cart"
        return redirect(link)
    else:
        return render_template("not_a_user.html")
        
@app.route("/<int:userid>/purchase/<int:cartid>")
def purchase(userid, cartid):
    user = User.query.filter_by(userid = userid).first()
    if(user):
        cart = Cart.query.filter_by(cartid = cartid).first()
        product = Product.query.filter_by(productid = cart.productid).first()
        product.quantity = product.quantity - cart.quantity
        cart.buy = 1
        db.session.commit()
        link = "/" + str(userid) + "/cart"
        return redirect(link)
    else:
        return render_template("not_a_user.html")
        
@app.route("/<int:userid>/buyall")
def buyall(userid):
    user = User.query.filter_by(userid = userid).first()
    if(user):
        cart = Cart.query.filter_by(userid = userid, buy = 0).all()
        for i in cart:
            product = Product.query.filter_by(productid = i.productid).first()
            if(product.quantity > 0):
                product.quantity = product.quantity - i.quantity
                i.buy = 1
        db.session.commit()
        link = "/" + str(userid) + "/profile"
        return redirect(link)
    else:
        return render_template("not_a_user.html")