from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    place_name = db.Column(db.String(255), nullable=False)
    business_details = db.Column(db.Text)
    selected_govs = db.Column(db.String(255), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Awaiting Payment Confirmation')
    json_file_url = db.Column(db.String(255))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'place_name': self.place_name,
            'business_details': self.business_details,
            'selected_govs': self.selected_govs,
            'total_price': self.total_price,
            'status': self.status,
            'json_file_url': self.json_file_url,
            'order_date': self.order_date.isoformat(),
        }
