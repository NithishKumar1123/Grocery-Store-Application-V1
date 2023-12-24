from .database import db

class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    isadmin = db.Column(db.Integer, nullable = False, default = 0)
    cart = db.relationship('Cart', backref = "user_", cascade = "all, delete-orphan")
    def __repr__(self):
        return '<User %r>' % self.username

class Category(db.Model):
    __tablename__ = 'category'
    categoryid = db.Column(db.Integer, autoincrement = True, primary_key = True)
    categoryname = db.Column(db.String, unique = True, nullable = False)
    products = db.relationship('Product', backref = "category_", lazy = True, cascade = "all, delete-orphan")
    def __repr__(self):
        return '<Category %r>' % self.categoryname

class Product(db.Model):
    __tablename__ = 'product'
    productid = db.Column(db.Integer, autoincrement = True, primary_key = True)
    productname = db.Column(db.String, nullable = False)
    price = db.Column(db.Float, nullable = False)
    unit = db.Column(db.String)
    quantity = db.Column(db.Integer, nullable = False)
    categoryid = db.Column(db.Integer, db.ForeignKey('category.categoryid'), nullable = False)
    cart = db.relationship('Cart', backref = "product_", cascade = "all, delete-orphan")
    def __repr__(self):
        return '<Product %r>' % self.productname
        
class Cart(db.Model):
    __tablename__ = 'cart'
    cartid = db.Column(db.Integer, autoincrement = True, primary_key = True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'), nullable = False)
    productid = db.Column(db.Integer, db.ForeignKey('product.productid'), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    buy = db.Column(db.Integer, nullable = False,  default = 0)