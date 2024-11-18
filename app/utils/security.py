from app.models.user import User

def get_current_user(phone_number):
    # Query the User based on phone_number
    user = User.query.filter_by(phone_number=phone_number).first()

    # Optionally handle cases where user is not found
    if not user:
        return None  # Or handle differently based on your application logic

    return user
