def test_user_login(client):
    response = client.post('/user/login', json={'phone_number': '+1234567890'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data['data']
