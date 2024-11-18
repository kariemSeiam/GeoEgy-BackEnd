def test_user_model(client):
    from app.models.user import User
    user = User(phone_number='+1234567890')
    assert user.phone_number == '+1234567890'
    assert user.is_admin == False
