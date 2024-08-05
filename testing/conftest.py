import pytest
from config import app, db
from models import Merchant, Admin, Clerk, Store

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    testing_client = app.test_client()

    with app.app_context():
        db.create_all()
        yield testing_client
        db.drop_all()

@pytest.fixture(scope='module')
def init_database():
    with app.app_context():
        db.create_all()
        store = Store(name='Test Store', location='Test Location')
        db.session.add(store)
        db.session.commit()
        yield db
        db.drop_all()
