from config import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from sqlalchemy import DateTime 


class Merchant(SerializerMixin,db.Model):
    __tablename__ = "merchants"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    role = db.Column(db.String)
    _password_hash = db.Column(db.String)
    store_id = db.Column(db.Integer,db.ForeignKey("stores.id")) # Foreign key to store tables

    stores = db.relationship("Store",back_populates="merchant") # Relationship with store

    serialize_rules = ("-stores.merchant",) # Serialization rules

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password is not readable')
    
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
    

class Admin(SerializerMixin,db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    _password_hash = db.Column(db.String)
    invitation_token = db.Column(db.String, nullable=True)
    account_status = db.Column(db.String, default = "active")
    store_id = db.Column(db.Integer,db.ForeignKey("stores.id")) # Foreign key to store table
    role = db.Column(db.String)
    store = db.relationship("Store",back_populates = "admin") # Relationship with store
    requests = db.relationship("Request",back_populates = "admin") # Relationship with request

    serialize_rules = ("-store.admin","-requests.admin") # Serialization rules
    


    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password is not readable')
    
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
    

    

class Clerk(SerializerMixin,db.Model):
    __tablename__ = "clerks"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    _password_hash = db.Column(db.String)
    account_status = db.Column(db.String, default = "active")
    store_id = db.Column(db.Integer,db.ForeignKey("stores.id"))
    invitation_token = db.Column(db.String, nullable=True)
    role = db.Column(db.String)

    store = db.relationship("Store",back_populates = "clerks")
    requests = db.relationship("Request",back_populates = "clerk")
    salesReports = db.relationship("SalesReport", back_populates = "clerk")
    serialize_rules=("-store.clerk","-requests.clerk","-salesReports.clerk")


    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password is not readable')
    
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
    
    
    
class Store(SerializerMixin,db.Model):
    __tablename__= "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    
    merchant = db.relationship("Merchant",back_populates="stores")
    admin = db.relationship("Admin",back_populates="store") # Relationhip with admin
    clerks = db.relationship("Clerk",back_populates="store") # Relationship with clerk
    products = db.relationship("Product",back_populates="store") # Relationship with product
    requests = db.relationship("Request",back_populates = "store") #Relationship with request
    salesReports = db.relationship("SalesReport",back_populates = "store") # Relationship with sales report
    
    serialize_rules = ('-products', '-clerks', '-admin',"-merchant","-requests")


class Product(db.Model,SerializerMixin):
    __tablename__ = "products"
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


    store = db.relationship("Store",back_populates="products")
    request = db.relationship("Request", back_populates="product")
    salesReport = db.relationship("SalesReport",back_populates="product")

    serialize_rules = ("-store.products","-request")


class Request(db.Model,SerializerMixin):
    __tablename__ = "requests"
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    description = db.Column(db.String,default="Products out of stock")
    quantity = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    status = db.Column(db.String,default="Pending")
    clerk_id = db.Column(db.Integer, db.ForeignKey('clerks.id'))
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    

    clerk = db.relationship('Clerk',back_populates='requests')
    admin = db.relationship('Admin', back_populates="requests")
    product = db.relationship('Product', back_populates='request')
    store = db.relationship("Store",back_populates="requests")

    serialize_rules = ('-clerk.requests','-clerk.store', '-admin', '-product.request','-product.store','-product.salesReport',"-store")



class SalesReport(db.Model,SerializerMixin):
    __tablename__ = "salesReports"
    id = db.Column(db.Integer,primary_key = True)
    date = db.Column(db.DateTime, default=datetime.now)
    product_name = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    clerk_id = db.Column(db.Integer, db.ForeignKey("clerks.id"))
    quantity_sold = db.Column(db.Integer)
    quantity_in_hand = db.Column(db.Integer)
    profit = db.Column(db.Integer)

    product = db.relationship("Product",back_populates="salesReport")
    store = db.relationship("Store",back_populates="salesReports")
    clerk = db.relationship("Clerk",back_populates="salesReports")

    serialize_rules = ("-product","-store","-clerk.salesReports","-clerk.requests","-clerk.store")





