from controllers.database import db 
from controllers.database import func
#NEW#
from flask_security import UserMixin, RoleMixin 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True) 
    full_name = db.Column(db.String(50), unique = False,  nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    phone_number = db.Column(db.String(10), unique = True, nullable = False)
    password = db.Column(db.String(130), nullable = False)
    active = db.Column(db.Boolean(), default = True)

    fs_uniquifier = db.Column(db.String(255), unique = True, nullable = False)
    fs_token_uniquifier = db.Column(db.String(255), unique = True, nullable = True)

    roles=db.relationship('Role', secondary='user_role')

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(255))

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable = False)

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    prime_location = db.Column(db.String(200), nullable = False)
    address = db.Column(db.String(500), nullable = False)
    pincode = db.Column(db.String(6), unique = True, nullable = False)
    max_spots = db.Column(db.Integer, nullable = False)
    price = db.Column(db.String(50), nullable = False)

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable = False)
    spot_number = db.Column(db.String(10))
    status = db.Column(db.String(20), nullable = False, default = 'available')
    parking_lot = db.relationship('ParkingLot', backref='spots')

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    vehicle_number = db.Column(db.String(20), nullable = True)
    parking_timestamp = db.Column(db.DateTime(timezone=True), server_default = func.now(), nullable = False)
    leaving_timestamp = db.Column(db.DateTime, nullable = True)
    cost_per_unit_time = db.Column(db.Integer, nullable = False)
    total_cost = db.Column(db.Integer,nullable = True)
    status = db.Column(db.String(20), nullable =False, default = 'active')
    user = db.relationship('User', backref='reservations')
    spot = db.relationship('ParkingSpot', backref='reservations')
