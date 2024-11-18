from .. import db

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    province = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<Place {self.id}: {self.name}>'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'province': self.province
        }
