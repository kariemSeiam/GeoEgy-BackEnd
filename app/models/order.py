from .. import db

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    place = db.Column(db.String(255), nullable=False)
    province = db.Column(db.String(255), nullable=False)
    total_cost = db.Column(db.Integer, nullable=False)
    is_accepted = db.Column(db.Boolean, default=False)
    file_url = db.Column(db.String(255))

    def __repr__(self):
        return f'<Order {self.id}>'

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'place': self.place,
            'province': self.province,
            'total_cost': self.total_cost,
            'is_accepted': self.is_accepted,
            'file_url': self.file_url
        }
