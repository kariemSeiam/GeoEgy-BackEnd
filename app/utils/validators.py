import re

class ValidationError(Exception):
    pass

def validate_phone_number(phone_number):
    if not re.match(r'^\+?\d{10,15}$', phone_number):
        raise ValidationError('Invalid phone number format')
