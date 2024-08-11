import pytest
from test_models import Merchant, Store, Product
from test_config import app,db,bcrypt

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    testing_client = app.test_client()

    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    # Create a test store
    store = Store(name="Test Store", location="Test Location")
    db.session.add(store)
    db.session.commit()

    yield db

    db.drop_all()

@pytest.fixture(scope='module')
def new_merchant(init_database):
    merchant = Merchant(
        username="testmerchant",
        email="merchant@example.com",
        store_id=1
    )
    merchant.password_hash = bcrypt.generate_password_hash("password123").decode('utf-8')
    db.session.add(merchant)
    db.session.commit()

    return merchant

@pytest.fixture(scope='module')
def new_product(init_database):
    product = Product(
        brand_name="Brand A",
        product_name="Product A",
        payment_status="Not Paid",
        received_items=100,
        closing_stock=100,
        buying_price=50.0,
        selling_price=70.0,
        store_id=1
    )
    db.session.add(product)
    db.session.commit()

    return product

@pytest.fixture(scope='module')
def token(test_client, new_merchant):
    response = test_client.post('/login', json={
        "email": "merchant@example.com",
        "password": "password123",
        "role": "Merchant"
    })
    return response.json['access_token']