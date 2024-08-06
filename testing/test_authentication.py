
def test_signup_invalid_email(test_client, init_database):
    response = test_client.post('/auth/signup', json={
        'full_name': 'Test Merchant',
        'email': 'invalid_email',
        'role': 'Merchant',
        'store_id': 1,
        'password': 'password',
        'phone_number': '1234567890'
    })
    assert response.status_code == 400

def test_signup_missing_fields(test_client, mock_post):
        response = test_client.post('/auth/signup', json={
            'full_name': 'Test Merchant',
            'email': 'merchant@example.com',
            'role': 'Merchant',
            'password': 'password',
            'phone_number': '1234567890'
        })
        assert response.status_code == 400

def test_login_invalid_credentials(test_client, init_database):
        response = test_client.post('/auth/login', json={
            'email': 'merchant@example.com',
            'password': 'wrong_password',
            'role': 'Merchant'
        })
        assert response.status_code == 401
def test_login_missing_fields(test_client, init_database):
        response = test_client.post('/auth/login', json={
            'email': 'merchant@example.com',
            'role': 'Merchant'
        })
        assert response.status_code == 400
    
    