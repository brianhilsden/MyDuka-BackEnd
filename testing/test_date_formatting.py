from datetime import datetime

def test_date_formatting(test_client, init_database):
    response = test_client.post('/sales/1', json={
        'date': datetime.now().isoformat(),
        'product_name': 'Test Product',
        'quantity': 10,
        'total_price': 100.0
    })
    assert response.status_code == 200

    sales_response = response.json['salesReport']
    assert 'date' in sales_response
    assert isinstance(sales_response['date'], str)  # Ensure date is in string format
