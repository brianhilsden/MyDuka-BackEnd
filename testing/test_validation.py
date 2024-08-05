def test_signup_validation(test_client, init_database):
    response = test_client.post('/signup', json={
        'full_name': '',
        'email': 'merchant3@example.com',
        'role': 'Merchant',
        'store_id': 1,
        'password': 'password'
    })
    assert response.status_code == 400
    assert 'error' in response.json

def test_login_validation(test_client, init_database):
    response = test_client.post('/login', json={
        'email': 'merchant3@example.com',
        'password': 'wrongpassword',
        'role': 'Merchant'
    })
    assert response.status_code == 401
    assert 'error' in response.json
