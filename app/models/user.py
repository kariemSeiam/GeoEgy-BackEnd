from .. import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.phone_number}>'

    def serialize(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'is_admin': self.is_admin,
            'orders': [order.serialize() for order in self.orders]
        }
