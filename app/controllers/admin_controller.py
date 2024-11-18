from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.user import User
from app.models.order import Order
from app.models.governorate import Governorate
from app.utils.security import admin_required
from app.utils.whatsapp import send_whatsapp_message
from app import db

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@bp.route('/orders', methods=['GET'])
@jwt_required()
@admin_required
def view_orders():
    orders = Order.query.all()
    return jsonify({'code': 200, 'message': 'Success', 'data': [order.serialize() for order in orders]})

@bp.route('/orders/<int:order_id>/send_message', methods=['POST'])
@jwt_required()
@admin_required
def send_order_message(order_id):
    order = Order.query.get_or_404(order_id)
    user = User.query.get(order.user_id)
    message = f"Dear {user.phone_number}, your order #{order.id} is awaiting payment. Please pay to Vodafone Cash number XYZ."
    send_whatsapp_message(user.whatsapp_number or user.phone_number, message)
    return jsonify({'code': 200, 'message': 'Message sent', 'data': {}})

@bp.route('/orders/<int:order_id>/accept', methods=['POST'])
@jwt_required()
@admin_required
def accept_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = 'Payment Confirmed'
    db.session.commit()
    return jsonify({'code': 200, 'message': 'Order accepted', 'data': order.serialize()})

@bp.route('/orders/<int:order_id>/complete', methods=['POST'])
@jwt_required()
@admin_required
def complete_order(order_id):
    data = request.get_json()
    json_file_url = data.get('json_file_url')
    order = Order.query.get_or_404(order_id)
    order.json_file_url = json_file_url
    order.status = 'Completed'
    db.session.commit()
    # Notify user
    user = User.query.get(order.user_id)
    message = f"Your order #{order.id} is completed. Access your data here: {json_file_url}"
    send_whatsapp_message(user.whatsapp_number or user.phone_number, message)
    return jsonify({'code': 200, 'message': 'Order completed', 'data': order.serialize()})

@bp.route('/users/<int:user_id>/block', methods=['POST'])
@jwt_required()
@admin_required
def block_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_blocked = True
    db.session.commit()
    return jsonify({'code': 200, 'message': 'User blocked', 'data': {}})

@bp.route('/users/<int:user_id>/unblock', methods=['POST'])
@jwt_required()
@admin_required
def unblock_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_blocked = False
    db.session.commit()
    return jsonify({'code': 200, 'message': 'User unblocked', 'data': {}})

@bp.route('/orders/<int:order_id>/delete', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'code': 200, 'message': 'Order deleted', 'data': {}})

@bp.route('/governorates', methods=['GET', 'POST'])
@jwt_required()
@admin_required
def manage_governorates():
    if request.method == 'GET':
        govs = Governorate.query.all()
        return jsonify({'code': 200, 'message': 'Success', 'data': [gov.serialize() for gov in govs]})
    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        gov = Governorate(name=name, price=price)
        db.session.add(gov)
        db.session.commit()
        return jsonify({'code': 201, 'message': 'Governorate added', 'data': gov.serialize()})
