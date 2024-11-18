from flask import Blueprint, jsonify, request, abort
from app.models.user import  User
from app.models.order import  Order
from app.utils.security import get_current_user
from .. import db

bp = Blueprint('order', __name__, url_prefix='/order')

@bp.route('/place', methods=['POST'])
def place_order():
    data = request.json
    user_id = data.get('user_id')
    place = data.get('place')
    province = data.get('province')
    total_cost = data.get('total_cost')

    new_order = Order(user_id=user_id, place=place, province=province, total_cost=total_cost)
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order placed successfully'})

@bp.route('/get_orders', methods=['GET'])
def get_orders():
    query = request.args.get('phone_number')
    current_user = get_current_user(query)  # Example: Implement authentication logic
    if current_user.is_admin:
        orders = Order.query.all()
    else:
        orders = Order.query.filter_by(user_id=current_user.id).all()

    return jsonify({'orders': [order.serialize() for order in orders]})

@bp.route('/accept_order/<int:order_id>', methods=['POST'])
def accept_order(order_id):
    current_user = get_current_user()  # Example: Implement authentication logic
    if not current_user.is_admin:
        abort(403)  # Unauthorized

    order = Order.query.get_or_404(order_id)
    order.is_accepted = True

    # Additional data for user's order history via JSON link
    json_link = request.json.get('json_link')
    if json_link:
        order.file_url = json_link

    selected_province = request.json.get('province')
    if selected_province:
        order.province = selected_province

    db.session.commit()

    # Send order confirmation via WhatsApp to user
    user = User.query.get(order.user_id)
    message = f"Your order for {order.place} has been accepted. Please check your dashboard."

    return jsonify({'message': 'Order accepted and user updated successfully'})
