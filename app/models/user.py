from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    whatsapp_number = db.Column(db.String(20))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    is_blocked = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='user', lazy=True)
    search_histories = db.relationship('SearchHistory', backref='user', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'whatsapp_number': self.whatsapp_number,
            'creation_date': self.creation_date.isoformat(),
            'is_admin': self.is_admin,
            'is_blocked': self.is_blocked,
        }
