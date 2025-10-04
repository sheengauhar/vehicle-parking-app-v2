from flask import current_app as app
from controllers.database import db
from controllers.models import User, Role, UserRole, ParkingLot 
from controllers.user_datastore import user_datastore



def create_tables():
    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name = 'admin', description = 'Administrator')
        user_role = user_datastore.find_or_create_role(name = 'user', description = 'Regular User')
        
        if not user_datastore.find_user(email = 'admin@gmail.com'):
            user_datastore.create_user(
                full_name = 'admin',
                email = 'admin@gmail.com',
                password = 'admin123',
                phone_number = '0000000000',
                roles=[admin_role]
            )
        
        '''if not user_role:
            user_role = Role(name = 'user')
            db.session.add(user_role)

        if not admin_role:
            admin_role = Role(name = 'admin')
            db.session.add(admin_role)'''

        db.session.commit()

        '''admin = User.query.filter_by(email = 'admin@gmail.com').first()
        if not admin:
            admin = User(
                full_name = 'admin',
                email = 'admin@gmail.com',
                password = 'admin123',
                phone_number = '0000000000',
                roles=[admin_role]
            )'''
            
        '''db.session.add(admin)
        
        db.session.commit()'''

