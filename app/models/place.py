from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    about = db.Column(db.Text)
    place_id = db.Column(db.String(100), unique=True)
    # Address fields
    formatted_address = db.Column(db.String(255))
    street = db.Column(db.String(100))
    locality = db.Column(db.String(100))
    district = db.Column(db.String(100))
    governorate = db.Column(db.String(100))
    # Coordinates
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    # Contact info
    phone_number = db.Column(db.String(20))
    url = db.Column(db.String(255))
    image = db.Column(db.String(255))
    # Operating hours
    status = db.Column(db.String(50))
    next_opening = db.Column(db.String(50))
    hours_next_open = db.Column(db.String(50))
    time_open = db.Column(db.String(50))
    # Reviews
    reviews_url = db.Column(db.String(255))
    reviews_count = db.Column(db.Integer)
    average_rating = db.Column(db.Float)
    # Additional info
    time_zone = db.Column(db.String(50))
    google_local_guide = db.Column(db.String(255))
    category = db.Column(db.String(50))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'about': self.about,
            'place_id': self.place_id,
            'address': {
                'formatted_address': self.formatted_address,
                'street': self.street,
                'locality': self.locality,
                'district': self.district,
                'governorate': self.governorate,
            },
            'coordinates': {
                'latitude': self.latitude,
                'longitude': self.longitude,
            },
            'phone_number': self.phone_number,
            'url': self.url,
            'image': self.image,
            'operating_hours': {
                'status': self.status,
                'next_opening': self.next_opening,
                'hours': {
                    'next_open': self.hours_next_open,
                    'time_open': self.time_open,
                },
            },
            'reviews': {
                'url': self.reviews_url,
                'count': self.reviews_count,
                'average_rating': self.average_rating,
            },
            'additional_info': {
                'time_zone': self.time_zone,
                'google_local_guide': self.google_local_guide,
                'category': self.category,
            },
        }
