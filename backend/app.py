from flask import Flask
from flask_restful import Api 
from flask_security import Security
from flask_cors import CORS

from controllers.create_database_instance import create_tables
from controllers.database import db
from controllers.config import Config
from controllers.user_datastore import user_datastore

from cache_instance import cache 


def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    Security(app, user_datastore)

    api = Api(app, prefix='/api')
    

    CORS(app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authentication-Token"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    cache.init_app(app, config={
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
    })

    app.app_context().push()
    return app,api

    
app, api = create_app()

# AUTH APIs

from controllers.authentication_apis import LoginAPI, LogoutAPI, RegisterAPI, CheckEmailAPI

api.add_resource(LoginAPI, '/login') #endpoint
api.add_resource(LogoutAPI, '/logout')
api.add_resource(RegisterAPI, '/register')
api.add_resource(CheckEmailAPI, '/check-email')

# CRUD APIs
from controllers.crud_api import ParkingLotAPI,AdminUsers, Profile, EditProfile, UserReservations, ParkingLotsList, NextAvailableSpot, CreateReservation, ReleaseReservation, ClearHistory, ViewUserBySpot, AdminRevenueSummary, AdminSpotStatusSummary,UserSpotUsagePerLot, ExportCSV
api.add_resource(ParkingLotAPI, '/parking_lots', '/parking_lots/<int:lot_id>')
api.add_resource(AdminUsers, '/admin/users')
api.add_resource(Profile, '/profile')
api.add_resource(EditProfile, '/profile/edit')
api.add_resource(UserReservations, '/user/reservations')
api.add_resource(ParkingLotsList, '/parking_lots')               # GET list
api.add_resource(NextAvailableSpot, '/parking_lots/<int:lot_id>/next_spot')
api.add_resource(CreateReservation, '/reservations') 
api.add_resource(ReleaseReservation, '/reservations/<int:reservation_id>/release') 
api.add_resource(ClearHistory, "/user/clear_history")
api.add_resource(ViewUserBySpot, "/spot/<int:spot_id>/user_info")
api.add_resource(AdminRevenueSummary, "/admin/summary/revenue")
api.add_resource(AdminSpotStatusSummary, "/admin/summary/spot_status")
api.add_resource(UserSpotUsagePerLot, "/user/summary/usage_per_lot")
api.add_resource(ExportCSV, "/export_csv")


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
