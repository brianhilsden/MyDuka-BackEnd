#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker

from config import app, db
from models import  Store, User, Product, Request

fake = Faker()

with app.app_context():

    print("Deleting all records...")
    Request.query.delete()
    Product.query.delete()
    User.query.delete()
    Store.query.delete()

    print("Creating stores...")
    stores = []
    for _ in range(5):
        store = Store(
            name=fake.company(),
            location=fake.address()
        )
        stores.append(store)

    db.session.add_all(stores)
    db.session.commit()

    print("Creating users...")
    users = []
    usernames = []
    for _ in range(20):
        username = fake.first_name()
        while username in usernames:
            username = fake.first_name()
        usernames.append(username)

        user = User(
            username=username,
            email=fake.email(),
            role=rc(['admin', 'clerk']),
            store_id=rc([store.id for store in stores])
        )
        user.password_hash = user.username + 'password'
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    print("Assigning store admins...")
    for store in stores:
        admin = rc([user for user in users if user.role == 'admin'])
        store.admin_id = admin.id

    db.session.add_all(stores)
    db.session.commit()

    print("Creating products...")
    products = []
    for _ in range(50):
        product = Product(
            brand_name=fake.company(),
            product_name=fake.word(),
            payment_status=rc(['paid', 'unpaid']),
            closing_stock=randint(1, 100),
            buying_price=round(fake.random_number(digits=5), 2),
            selling_price=round(fake.random_number(digits=5), 2),
            store_id=rc([store.id for store in stores])
        )
        products.append(product)

    db.session.add_all(products)
    db.session.commit()

    print("Creating requests...")
    requests = []
    for _ in range(100):
        request = Request(
            description=fake.sentence(),
            product_id=rc([product.id for product in products]),
            clerk_id=rc([user.id for user in users if user.role == 'clerk']),
            admin_id=rc([user.id for user in users if user.role == 'admin'])
        )
        requests.append(request)

    db.session.add_all(requests)
    db.session.commit()

    print("Complete.")
