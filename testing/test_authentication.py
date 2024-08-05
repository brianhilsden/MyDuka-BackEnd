import pytest
from flask import url_for

def test_signup(test_client, init_database):
    response = test_client.post('/signup', json={
        'full_name': 'Test Merchant',
        'email': 'merchant@example.com',
        'role': 'Merchant',
        'store_id': 1,
        'password': 'password',
        'phone_number': '1234567890'
    })
    assert response.status_code == 201

    # Check if email with token was sent
    # Simulate token verification

def test_login(test_client, init_database):
    response = test_client.post('/login', json={
        'email': 'merchant@example.com',
        'password': 'password',
        'role': 'Merchant'
    })
    assert response.status_code == 201
    assert 'access_token' in response.json
