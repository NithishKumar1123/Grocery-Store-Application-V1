from flask import request, redirect, render_template
from flask import current_app as app
from application.database import db
from application.models import User, Category, Product, Cart

# APP

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/logout")
def logout():
    return render_template("logout.html")

# CATEGORY

@app.route("/<int:userid>/category")
def category(userid):
    user = User.query.filter_by(userid = userid).first()
    if(user):
        category = Category.query.all()
        return render_template("category.html", user = user, category = category)
    else:
        return render_template("not_an_admin.html")

@app.route("/<int:userid>/csearch/<search>")
def csearch(userid, search):
    user = User.query.filter_by(userid = userid).first()
    if(user):
        like = "%" + search + "%"
        category = Category.query.filter(Category.categoryname.like(like)).all()
        return render_template("search_category.html", user = user, category = category, search = search)
    else:
        return render_template("not_an_admin.html")

# PRODUCT

@app.route("/<int:userid>/category/<int:categoryid>/product")
def products(userid, categoryid):
    user = User.query.filter_by(userid = userid).first()
    if(user):
        category = Category.query.filter_by(categoryid = categoryid).first()
        return render_template("products.html", user = user, category = category)
    else:
        return render_template("not_an_admin.html")

@app.route("/<int:userid>/product/<int:productid>", methods = ["GET", "POST"])
def product(userid, productid):
    if request.method == "GET":
        user = User.query.filter_by(userid = userid).first()
        if(user):
            product = Product.query.filter_by(productid = productid).first()
            cart = Cart.query.filter_by(userid = userid, productid = productid).first()
            return render_template("product.html", user = user, product = product, cart = cart)
        else:
            return render_template("not_an_admin.html")
    else:
        user = User.query.filter_by(userid = userid).first()
        if(user):
            quantity = request.form["quantity"]
            cart = Cart(userid = userid, productid = productid, quantity = quantity)
            db.session.add(cart)
            db.session.commit()
            link = "/" + str(userid) + "/cart"
            return redirect(link)
        
@app.route("/<int:userid>/read_product")
def read_product(userid):
    user = User.query.filter_by(userid = userid).first()
    if(user):
        category = Category.query.all()
        return render_template("read_product.html", user = user, category = category)
    else:
        return render_template("not_an_admin.html")
        

@app.route("/<int:userid>/psearch/<search>")
def psearch(userid, search):
    user = User.query.filter_by(userid = userid).first()
    if(user):
        like = "%" + search + "%"
        product = Product.query.filter(Product.productname.like(like)).all()
        return render_template("search_product.html", user = user, product = product, search = search)
    else:
        return render_template("not_an_admin.html")

@app.route("/<int:userid>/<search>/<int:sort>")
def sortproduct(userid, search, sort):
    user = User.query.filter_by(userid = userid).first()
    if(user):
        like = "%" + search + "%"
        if(sort == 0):
            product = Product.query.filter(Product.productname.like(like)).order_by(Product.price).all()
        else:
            product = Product.query.filter(Product.productname.like(like)).order_by(Product.price.desc()).all()
        return render_template("search_product.html", user = user, product = product, search = search)
    else:
        return render_template("not_an_admin.html")

# CART

@app.route("/<int:userid>/cart")
def cart(userid):
    user = User.query.filter_by(userid = userid).first()
    if(user):
        cart = Cart.query.filter_by(userid = userid, buy = 0).all()
        c = db.session.execute(db.select(Cart.productid, db.func.sum(Cart.quantity)).filter_by(buy = 0, userid = userid).group_by(Cart.productid)).fetchall()
        total = 0
        for i in c:
            p = Product.query.filter_by(productid = i[0]).first()
            if(p.quantity > 0):
                total = total + (i[1] * p.price)
        return render_template("cart.html", user = user, cart = cart, total = total)
    else:
        return render_template("not_an_admin.html")