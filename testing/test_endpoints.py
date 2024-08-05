def test_get_specific_store_products(test_client, init_database):
    response = test_client.get('/getProducts/1')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_sales_post(test_client, init_database):
    response = test_client.post('/sales/1', json={
        'date': '2024-08-05',
        'product_name': 'Test Product',
        'quantity': 10,
        'total_price': 100.0
    })
    assert response.status_code == 200
    assert 'message' in response.json
