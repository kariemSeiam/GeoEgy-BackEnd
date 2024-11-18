def test_validate_phone_number():
    from app.utils.validators import validate_phone_number
    validate_phone_number('+1234567890')
