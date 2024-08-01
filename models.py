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
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    admin = db.relationship('User', back_populates='admin_store', foreign_keys=[admin_id])
    clerks = db.relationship('User', back_populates='clerk_store', foreign_keys='User.store_id')
    products = db.relationship('Product', back_populates = 'store')

    serialize_rules = ('-products.store', '-clerks.clerks_store', '-admin.admin_store' )


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    account_status = db.Column(db.String, default='active')
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    admin_store = db.relationship('Store', back_populates='admin', foreign_keys=[Store.admin_id])
    clerk_store = db.relationship('Store', back_populates='clerks', foreign_keys=[store_id])
    requests = db.relationship('Request', back_populates='user')

    serialize_rules = ('-admin_store.admin', '-clerk_store.clerks', '-requests.user')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password is not readable')
    
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
    
    



class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String, nullable=False)
    product_name = db.Column(db.String, nullable=False)
    availability = db.Column(db.Boolean, default=True)
    payment_status = db.Column(db.String, nullable=False)
    closing_stock = db.Column(db.Integer, nullable=False)
    buying_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)

    store = db.relationship('Store', back_populates = 'products')

    serialize_rules = ('-store.products',)

class Request(db.Model, SerializerMixin):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    description = db.Column(db.String, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    clerk_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='requests', foreign_keys=[clerk_id])
    admin = db.relationship('User', foreign_keys=[admin_id])
    product = db.relationship('Product', back_populates='requests')

    serialize_rules = ('-user.requests', '-admin.requests', '-product.requests')





