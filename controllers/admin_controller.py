from flask import request, redirect, render_template
from flask import current_app as app
from application.database import db
from application.models import User, Category, Product, Cart
import matplotlib.pyplot as plt

# ADMIN

@app.route("/admin_login", methods = ["GET", "POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin_login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username = username, password = password, isadmin = 1).first()
        if(user):
            link = "/admin_dashboard/" + str(user.userid)
            return redirect(link)
        else:
            return render_template("not_an_admin.html")
            
@app.route("/admin_dashboard/<int:userid>")
def admin_dashboard(userid):
    user = User.query.filter_by(userid = userid, isadmin = 1).first()
    if(user):
        
        # CHART - 1
        
        category = db.session.execute(db.select(Product.categoryid, db.func.count(Product.categoryid)).group_by(Product.categoryid).order_by(db.func.count(Product.categoryid).desc())).fetchall()
        categorylabel = []
        productcount = []
        for i in category:
            c = Category.query.filter_by(categoryid = i[0]).first()
            categorylabel.append(c.categoryname)
            productcount.append(i[1])
        cat = Category.query.all()
        for i in cat:
            if(i.categoryname not in categorylabel):
                categorylabel.append(i.categoryname)
                productcount.append(0)
        plt.figure(figsize = (9, 5))
        plt.bar(categorylabel[:4], productcount[:4])
        plt.xlabel("Category", fontweight = "bold")
        plt.ylabel("Number of Products", fontweight = "bold")
        plt.title("Number of Products in each Category", fontweight = "bold")
        plt.savefig('static/category.jpg')
        
        # CHART - 2
        
        products = db.session.execute(db.select(Product.productname, Product.quantity).order_by(Product.quantity.desc())).fetchall()
        productlabel = []
        quantity = []
        for i in products:
            productlabel.append(i[0])
            quantity.append(i[1])
        plt.figure(figsize = (12, 5))
        plt.bar(productlabel[:4], quantity[:4])
        plt.xlabel("Product", fontweight = "bold")
        plt.ylabel("Quantity", fontweight = "bold")
        plt.title("Product Stocks", fontweight = "bold")
        plt.savefig('static/product.jpg')
        
        products = db.session.execute(db.select(Product.productname).filter_by(quantity = 0)).fetchall()
        pro = []
        for i in products:
            pro.append(i[0])
            
        cart = db.session.execute(db.select(Cart.productid, db.func.sum(Cart.quantity)).filter_by(buy = 1).group_by(Cart.productid)).fetchall()
        max = -1
        maxele = 0
        for i in cart:
            if i[1] > max:
                max = i[1]
                maxele = i[0]
        pp = Product.query.filter_by(productid = maxele).first()
        
        u = len(User.query.all())
        pd = len(Product.query.all())
        c = len(Category.query.all())
        
        r = [u, pd, c]
        
        return render_template("admin_dashboard.html", user = user, p = pro, pp = pp, max = max, r = r)
    else:
        return render_template("not_an_admin.html")

# CATEGORY

@app.route("/<int:userid>/create_category", methods = ["GET", "POST"])
def create_category(userid):
    if request.method == "GET":
        user = User.query.filter_by(userid = userid, isadmin = 1).first()
        if(user):
            return render_template("create_category.html", user = user)
        else:
            return render_template("not_an_admin.html")
    else:
        categoryname = request.form["categoryname"]
        category = Category(categoryname = categoryname)
        db.session.add(category)
        db.session.commit()
        link = "/" + str(userid) + "/category"
        return redirect(link)

@app.route("/<int:userid>/update_category/<int:categoryid>", methods = ["GET", "POST"])
def update_category(userid, categoryid):
    if request.method == "GET":
        user = User.query.filter_by(userid = userid, isadmin = 1).first()
        if(user):
            category = Category.query.filter_by(categoryid = categoryid).first()
            return render_template("update_category.html", user = user, category = category)
        else:
            return render_template("not_an_admin.html")
    else:
        categoryname = request.form["categoryname"]
        category = Category.query.filter_by(categoryid = categoryid).first()
        category.categoryname = categoryname
        db.session.commit()
        link = "/" + str(userid) + "/category"
        return redirect(link)
        
@app.route("/<int:userid>/delete_category/<int:categoryid>")
def delete_category(userid, categoryid):
    user = User.query.filter_by(userid = userid, isadmin = 1).first()
    if(user):
        category = Category.query.filter_by(categoryid = categoryid).first()
        db.session.delete(category)
        db.session.commit()
        link = "/" + str(userid) + "/category"
        return redirect(link)
    else:
        return render_template("not_an_user.html")

# PRODUCT

@app.route("/<int:userid>/create_product", methods = ["GET", "POST"])
def create_product(userid):
    if request.method == "GET":
        user = User.query.filter_by(userid = userid, isadmin = 1).first()
        if(user):
            category = Category.query.all()
            return render_template("create_product.html", user = user, category = category)
        else:
            return render_template("not_an_admin.html")
    else:
        productname = request.form["productname"]
        price = request.form["price"]
        unit = request.form["unit"]
        quantity = request.form["quantity"]
        category = request.form["category"]
        category = Category.query.filter_by(categoryname = category).first()
        product = Product(productname = productname, price = price, unit = unit, quantity = quantity, categoryid = category.categoryid)
        db.session.add(product)
        db.session.commit()
        link = "/" + str(userid) + "/read_product"
        return redirect(link)
        
@app.route("/<int:userid>/update_product/<int:productid>", methods = ["GET", "POST"])
def update_product(userid, productid):
    if request.method == "GET":
        user = User.query.filter_by(userid = userid, isadmin = 1).first()
        if(user):
            list = Category.query.all()
            product = Product.query.filter_by(productid = productid).first()
            return render_template("update_product.html", user = user, product = product, list = list)
        else:
            return render_template("not_an_admin.html")
    else:
        productname = request.form["productname"]
        price = request.form["price"]
        unit = request.form["unit"]
        quantity = request.form["quantity"]
        category = request.form["category"]
        category = Category.query.filter_by(categoryname = category).first()
        product = Product.query.filter_by(productid = productid).first()
        product.productname = productname
        product.price = price
        product.unit = unit
        product.quantity = quantity
        product.categoryid = category.categoryid
        db.session.commit()
        link = "/" + str(userid) + "/product/" + str(productid)
        return redirect(link)

@app.route("/<int:userid>/delete_product/<int:productid>")
def delete_product(userid, productid):
    user = User.query.filter_by(userid = userid, isadmin = 1).first()
    if(user):
        product = Product.query.filter_by(productid = productid).first()
        id = product.categoryid
        db.session.delete(product)
        db.session.commit()
        link = "/" + str(userid) + "/category/" + str(id) + "/product"
        return redirect(link)
    else:
        return render_template("not_an_user.html")