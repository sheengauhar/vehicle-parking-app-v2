from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import utils, auth_token_required, roles_required, current_user

from controllers.database import db
from controllers.models import *

from datetime import datetime 
import pytz 
india = pytz.timezone('Asia/Kolkata')

from sqlalchemy import text

from cache_instance import cache 

class ParkingLotAPI(Resource):
    @cache.cached(timeout=30, query_string=False)
    def get(self, lot_id = None):
        print("[CACHE] MISS for /parking_lots")
        if lot_id:
            Parkinglot = ParkingLot.query.get(lot_id)
            if not Parkinglot:
                return make_response(jsonify({'message': 'Parking Lot Not Found.'}), 404)
            
            occupied_spots = ParkingSpot.query.filter_by(lot_id=Parkinglot.id, status='occupied').count()

            response = {
                'id': Parkinglot.id,
                'prime_location': Parkinglot.prime_location,
                'address': Parkinglot.address,
                'pincode': Parkinglot.pincode,
                'max_spots': Parkinglot.max_spots,
                'price': Parkinglot.price,
                'occupied_spots': occupied_spots,
                'spots': [
                    {
                        'id': spot.id,
                        'spot_number': spot.spot_number,
                        'status': spot.status
                    }
                    for spot in ParkingSpot.query.filter_by(lot_id=Parkinglot.id).all()
                ]
            }
            return make_response(jsonify(response), 200)

        else:
            Parkinglots = ParkingLot.query.all()
            response=[]
            for lot in Parkinglots:
                occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='occupied').count()
                spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()

                response.append({
                    'id': lot.id,
                    'prime_location': lot.prime_location,
                    'address': lot.address,
                    'pincode': lot.pincode,
                    'max_spots': lot.max_spots,
                    'price': lot.price,
                    'occupied_spots': occupied,
                    'spots': [
                        {
                            'id': spot.id,
                            'spot_number': spot.spot_number,
                            'status': spot.status
                        }
                        for spot in spots
                    ]
                })
            return make_response(jsonify(response), 200)
    
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({'message': 'No input data provided.'}),400)
        
        prime_location = data.get('prime_location')
        address = data.get('address')
        pincode = data.get('pincode')
        max_spots = data.get('max_spots')
        price = data.get('price')

        if not prime_location or not address or not pincode or not max_spots or not price:
            return make_response(jsonify({'message': 'All fields are required.'}),400)
                
        try:
            max_spots = int(max_spots)
            price = float(price)
        except (TypeError, ValueError):
            return make_response(jsonify({'message': 'Please enter valid numbers for Max Spots and Price'}), 400)
        
        existing_lot = ParkingLot.query.filter_by(address=address, pincode=pincode).first()
        if existing_lot:
            return make_response(jsonify({'message': 'Parking Lot with this pincode already exists.'}),400)
        
        if len(str(pincode))<6 or len(str(pincode))>6:
            return make_response(jsonify({'message': 'Please enter valid pincode'}),400)
        
        if(max_spots<0):
            return make_response(jsonify({'message': 'Please enter valid number of spots'}),400)
        
        new_lot = ParkingLot(
            prime_location = prime_location,
            address = address,
            pincode = pincode,
            max_spots = max_spots,
            price = price
        )
        db.session.add(new_lot)
        db.session.commit()

        for i in range(1, max_spots+1):
            spot_id = f"A{i}"
            new_spot = ParkingSpot(lot_id=new_lot.id, spot_number=spot_id, status='available')
            db.session.add(new_spot)
        db.session.commit()
        cache.clear()

        response = {
            'message': 'Parking Lot created successfully!',
            'data':{
                'id' : new_lot.id,
                'prime_location' : new_lot.prime_location,
                'address' : new_lot.address,
                'pincode' : new_lot.pincode,
                'max_spots' : new_lot.max_spots,
                'price' : new_lot.price
            }
        }
        return make_response(jsonify(response), 201)
    
    @auth_token_required
    @roles_required('admin')
    def put(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return make_response(jsonify({'message': 'Parking Lot not found.'}), 404)

        data = request.get_json()
        if not data:
            return make_response(jsonify({'message': 'No input data provided.'}), 400)

        prime_location = data.get('prime_location')
        address = data.get('address')
        pincode = data.get('pincode')
        max_spots = data.get('max_spots')
        price = data.get('price')

        if max_spots is not None:
            try:
                max_spots = int(max_spots)
            except (TypeError, ValueError):
                return make_response(jsonify({'message': 'Invalid value for max_spots'}), 400)

        if price is not None:
            try:
                price = float(price)
            except (TypeError, ValueError):
                return make_response(jsonify({'message': 'Invalid value for price'}), 400)

        if pincode:
            existing = ParkingLot.query.filter(
                ParkingLot.pincode == pincode,
                ParkingLot.id != lot_id
            ).first()
            if existing:
                return make_response(jsonify({'message': 'Parking Lot with this pincode already exists.'}), 400)

        if max_spots is not None:
            occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='occupied').count()
            if max_spots < occupied_spots:
                return make_response(jsonify({
                    'message': f'Update failed: At least {occupied_spots} spots are currently occupied. Please adjust maximum spots accordingly.'
                }), 400)
            
        if prime_location:
            lot.prime_location = prime_location
        if address:
            lot.address = address
        if pincode:
            lot.pincode = pincode
        if max_spots is not None:
            lot.max_spots = max_spots
        if price is not None:
            lot.price = price

        existing_spots = ParkingSpot.query.filter_by(lot_id=lot.id).order_by(ParkingSpot.id).all()
        current_count = len(existing_spots)

        if max_spots is not None and max_spots > current_count:
            for i in range(current_count + 1, max_spots + 1):
                new_spot = ParkingSpot(
                    lot_id=lot.id,
                    spot_number=f"A{i}",
                    status='available'
                )
                db.session.add(new_spot)

        elif max_spots is not None and max_spots < current_count:
            removable = [s for s in reversed(existing_spots) if s.status != 'occupied']
            to_remove = current_count - max_spots
            if len(removable) < to_remove:
                to_remove = len(removable)
            for spot in removable[:to_remove]:
                db.session.delete(spot)

        db.session.commit()
        cache.clear()
        response = {
            'message': 'Parking Lot updated successfully!',
            'data': {
                'id': lot.id,
                'prime_location': lot.prime_location,
                'address': lot.address,
                'pincode': lot.pincode,
                'max_spots': lot.max_spots,
                'price': lot.price
            }
        }
        return make_response(jsonify(response), 200)
    
    @auth_token_required
    @roles_required('admin')
    def delete(self, lot_id):
        parkinglot = ParkingLot.query.get(lot_id)

        if not parkinglot:
            return make_response(jsonify({'message': 'Parking Lot not found.'}), 404)
        
        occupied_spots = ParkingSpot.query.filter_by(lot_id=parkinglot.id, status='occupied').count()
        if occupied_spots > 0:
            return make_response(jsonify({
                'message': f"Cannot delete this lot: {occupied_spots} spot(s) are still occupied."
            }), 400)
        
        spots = ParkingSpot.query.filter_by(lot_id=parkinglot.id).all()
        for spot in spots:
            db.session.delete(spot)

        
        db.session.delete(parkinglot)
        db.session.commit()
        cache.clear()

        response={
            'message': 'Parking Lot deleted successfully!'
        }
        return make_response(jsonify(response), 200)

class AdminUsers(Resource):
    def get(self):
        users = User.query.all()

        users_list = [{
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone_number": user.phone_number
        } for user in users]

        return {"users": users_list}, 200


class Profile(Resource):
    def get(self):
        if not current_user.is_authenticated:
            return {"message": "Not authenticated"}, 401

        return {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "phone_number": current_user.phone_number
        }, 200

class EditProfile(Resource):
    def put(self):
        if not current_user.is_authenticated:
            return {"message": "Not authenticated"}, 401

        data = request.json

        current_user.full_name = data.get("full_name", current_user.full_name)
        current_user.phone_number = data.get("phone_number", current_user.phone_number)

        db.session.commit()

        return {"message": "Profile updated successfully!"}, 200

def spot_to_dict(spot):
    return {
        "id": spot.id,
        "spot_number": getattr(spot, "spot_number", None) or getattr(spot, "number", None),
        "status": spot.status,
        "lot_id": spot.lot_id
    }


def reservation_to_dict(r):
    return {
        "id": r.id,
        "spot": {
            "id": r.spot.id,
            "spot_number": r.spot.spot_number,
            "parking_lot": {
                "id": r.spot.parking_lot.id,
                "prime_location": r.spot.parking_lot.prime_location,
                "pincode": r.spot.parking_lot.pincode
            }
        },
        "vehicle_number": r.vehicle_number,
        "parking_timestamp": r.parking_timestamp.isoformat() if r.parking_timestamp else None,
        "leaving_timestamp": r.leaving_timestamp.isoformat() if r.leaving_timestamp else None,
        "cost_per_unit_time": r.cost_per_unit_time,
        "total_cost": r.total_cost,
        "status": r.status
    }


class UserReservations(Resource):
    @auth_token_required 
    @roles_required('user')
    def get(self):
        if not current_user.is_authenticated:
            return {"message": "Not authenticated"}, 401

        reservations = Reservation.query.filter_by(user_id=current_user.id).order_by(Reservation.id.desc()).all()
        data = [reservation_to_dict(r) for r in reservations]
        return {"reservations": data}, 200


class ParkingLotsList(Resource):
    @auth_token_required
    @roles_required('user')
    @cache.cached(timeout=60, query_string=False)
    def get(self):
        print("[CACHE] MISS for /parking_lots")
        lots = ParkingLot.query.all()
        result = []
        for lot in lots:
            available_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='available').all()
            result.append({
                "lot": {
                    "id": lot.id,
                    "prime_location": lot.prime_location,
                    "address": lot.address,
                    "pincode": lot.pincode,
                    "max_spots": lot.max_spots,
                    "price": lot.price
                },
                "available_spots": [spot_to_dict(s) for s in available_spots]
            })
        return {"lot_data": result}, 200

class NextAvailableSpot(Resource):
    def get(self, lot_id):
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {"message": "Lot not found"}, 404

        spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='available').first()
        if not spot:
            return {"message": "No available spots"}, 404

        return {
            "lot": {
                "id": lot.id,
                "prime_location": lot.prime_location,
                "price": lot.price
            },
            "spot": spot_to_dict(spot),
            "current_time": datetime.now(india).strftime('%Y-%m-%dT%H:%M')
        }, 200


class CreateReservation(Resource):
    @auth_token_required
    @roles_required('user')
    def post(self):
        data = request.json or {}
        lot_id = data.get("lot_id")
        vehicle_number = data.get("vehicle_number")

        if not lot_id or not vehicle_number:
            return {"message": "lot_id and vehicle_number required"}, 400
        
        existing_reservation = Reservation.query.filter(Reservation.vehicle_number==vehicle_number, Reservation.leaving_timestamp==None).first()
        if existing_reservation:
            return{"message": "This Vehicle is already parked."},400

        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return {"message": "Lot not found"}, 404

        spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='available').first()
        if not spot:
            return {"message": "No available spots"}, 400
        
        spot.status = 'occupied'
        db.session.commit()

        parking_timestamp = datetime.now(india)

        reservation = Reservation(
            spot_id=spot.id,
            user_id=current_user.id,
            vehicle_number=vehicle_number,
            parking_timestamp=parking_timestamp,
            status='parked',
            cost_per_unit_time=lot.price,
            total_cost=0.0,
            leaving_timestamp=None
        )

        db.session.add(reservation)
        db.session.commit()
        cache.clear()

        return {
            "message": f"Successfully booked {spot.spot_number} in {lot.prime_location}",
            "reservation": reservation_to_dict(reservation)
        }, 201

class ReleaseReservation(Resource):
    @auth_token_required
    @roles_required('user')
    def post(self, reservation_id):
        reservation = Reservation.query.get(reservation_id)

        if not reservation or reservation.user_id != current_user.id:
            return {"message": "Reservation not found"}, 404

        if reservation.status != 'parked':
            return {"message": "Reservation already released"}, 400

        reservation.leaving_timestamp = datetime.now(india)
        # ensure timezone-aware subtraction if needed
        if reservation.parking_timestamp.tzinfo is None:
            reservation.parking_timestamp = india.localize(reservation.parking_timestamp)

        duration_hours = (reservation.leaving_timestamp - reservation.parking_timestamp).total_seconds() / 3600.0
        reservation.total_cost = round(duration_hours * reservation.cost_per_unit_time, 2)
        reservation.status = 'left'

        spot = ParkingSpot.query.get(reservation.spot_id)
        spot.status = 'available'

        db.session.commit()
        return {"message": f"Spot released. Total cost: ₹{reservation.total_cost}", "reservation": reservation_to_dict(reservation)}, 200
    
class ClearHistory(Resource):
    @auth_token_required
    @roles_required('user')
    def delete(self):
        deleted = Reservation.query.filter_by(
            user_id=current_user.id,
            status='left'
        ).delete()

        db.session.commit()
        cache.clear()
        

        return {"message": f"Cleared {deleted} past reservations!"}, 200

class ViewUserBySpot(Resource):

    @auth_token_required
    @roles_required('admin')
    def get(self, spot_id):

        spot = ParkingSpot.query.get(spot_id)
        if not spot:
            return {"message": "Spot not found"}, 404

        reservation = Reservation.query \
            .filter_by(spot_id=spot_id) \
            .order_by(Reservation.parking_timestamp.desc()) \
            .first()

        if not reservation:
            return {"message": "No reservation found"}, 404

        user = reservation.user

        return {
            "spot": {
                "id": spot.id,
                "spot_number": spot.spot_number
            },
            "reservation": {
                "vehicle_number": reservation.vehicle_number,
                "parking_timestamp": reservation.parking_timestamp.isoformat(),
                "status": reservation.status,
                "cost_per_unit_time": reservation.cost_per_unit_time
            },
            "user": {
                "full_name": user.full_name,
                "email": user.email,
                "phone_number": user.phone_number
            }
        }, 200
    

class AdminRevenueSummary(Resource):
    @auth_token_required
    @roles_required('admin')
    @cache.cached(timeout=120, query_string=False)
    def get(self):
        print("[CACHE] MISS for /admin/revenue/summary")
        query = text("""
            SELECT parking_lot.prime_location, SUM(reservation.total_cost)
            FROM reservation
            JOIN parking_spot ON reservation.spot_id = parking_spot.id
            JOIN parking_lot ON parking_spot.lot_id = parking_lot.id
            GROUP BY parking_lot.prime_location
        """)
        results = db.session.execute(query).fetchall()

        labels = [row[0] for row in results]
        values = [float(row[1]) if row[1] else 0 for row in results]

        return {"labels": labels, "values": values}, 200
    
class AdminSpotStatusSummary(Resource):
    @auth_token_required
    @roles_required('admin')
    @cache.cached(timeout=120, query_string=False)
    def get(self):
        print("[CACHE] MISS for /admin/summary/spot_status")
        lots = ParkingLot.query.all()
        
        labels = []
        occupied = []
        available = []

        for lot in lots:
            labels.append(lot.prime_location)
            occ = ParkingSpot.query.filter_by(lot_id=lot.id, status='occupied').count()
            ava = ParkingSpot.query.filter_by(lot_id=lot.id, status='available').count()
            occupied.append(occ)
            available.append(ava)

        return {
            "labels": labels,
            "occupied": occupied,
            "available": available
        }, 200


class UserSpotUsagePerLot(Resource):
    @auth_token_required
    @roles_required('user')
    @cache.cached(timeout=60, query_string=False)
    def get(self):
        print("[CACHE] MISS for /user/spot-usage-per-lot")
        query = text("""
            SELECT 
                parking_lot.prime_location,
                parking_spot.spot_number,
                COUNT(reservation.id) AS usage_count
            FROM reservation
            JOIN parking_spot ON reservation.spot_id = parking_spot.id
            JOIN parking_lot ON parking_spot.lot_id = parking_lot.id
            WHERE reservation.status = 'left'
            GROUP BY parking_lot.prime_location, parking_spot.spot_number
            ORDER BY parking_lot.prime_location, parking_spot.spot_number
        """)

        rows = db.session.execute(query).fetchall()

        response = {}
        for lot, spot, count in rows:
            response.setdefault(lot, []).append({
                "spot": spot,
                "count": count
            })

        return [{"lot": lot, "spots": spots} for lot, spots in response.items()]


class ExportCSV(Resource):
    @auth_token_required
    @roles_required('user')
    def post(self):
        from celery_app import generate_user_csv
        user = current_user 
        
        generate_user_csv.delay(user.id, user.email)

        return {
            "message": "CSV export started. You will receive an email shortly."
        }, 202