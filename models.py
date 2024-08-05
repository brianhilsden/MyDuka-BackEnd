from config import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from sqlalchemy import DateTime 

class Store(db.Model, SerializerMixin):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    admin = db.relationship('User', back_populates='admin_store', foreign_keys=[admin_id])
    clerks = db.relationship('User', back_populates='clerk_store', foreign_keys='User.store_id')
    products = db.relationship('Product', back_populates='store')
    requests = db.relationship("Request",back_populates = "store")
    salesReports = db.relationship("SalesReport",back_populates="store")

    serialize_rules = ('-products.store', '-clerks.clerk_store', '-admin.admin_store',"-requests.store","-salesReports")

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String, nullable=False)
    product_name = db.Column(db.String, nullable=False)
    availability = db.Column(db.Boolean, default=True)
    payment_status = db.Column(db.String, nullable=False)
    received_items = db.Column(db.Integer)
    closing_stock = db.Column(db.Integer, nullable=False)
    spoilt_items = db.Column(db.Integer,default=0)
    buying_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)

    store = db.relationship('Store', back_populates='products')
    requests = db.relationship('Request', back_populates='product')
    salesReport = db.relationship("SalesReport",back_populates="product")

    serialize_rules = ('-store',"-requests","-salesReport")


"""To be reviewed"""
class Request(db.Model, SerializerMixin):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    description = db.Column(db.String,default="Products out of stock")
    quantity = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    clerk_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    

    user = db.relationship('User', foreign_keys=[clerk_id], back_populates='requests')
    admin = db.relationship('User', foreign_keys=[admin_id])
    product = db.relationship('Product', back_populates='requests')
    store = db.relationship("Store",back_populates="requests")

    serialize_rules = ('-user', '-admin', '-product',"-store")

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    account_status = db.Column(db.String, default='active')
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    admin_store = db.relationship('Store', back_populates='admin', foreign_keys=[Store.admin_id])
    clerk_store = db.relationship('Store', back_populates='clerks', foreign_keys=[store_id])
    requests = db.relationship('Request', foreign_keys=[Request.clerk_id], back_populates='user', lazy=True)

    serialize_rules = ('-admin_store.admin', '-clerk_store', '-requests')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password is not readable')
    
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))


class SalesReport(db.Model,SerializerMixin):
    __tablename__ = "salesReport"
    id = db.Column(db.Integer,primary_key = True)
    date = db.Column(db.DateTime, default=datetime.now)
    product_name = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    quantity_sold = db.Column(db.Integer)
    quantity_in_hand = db.Column(db.Integer)
    profit = db.Column(db.Integer)

    product = db.relationship("Product",back_populates="salesReport")
    store = db.relationship("Store",back_populates="salesReports")

    serialize_rules = ("-product","-store")