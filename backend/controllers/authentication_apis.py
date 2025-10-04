from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_security import utils, auth_token_required #to verify the passwords 





from controllers.user_datastore import user_datastore
from controllers.database import db

class LoginAPI(Resource):
    def post(self):
        login_credentials = request.get_json() #To get any data sent by an api

        #data validation
        if not login_credentials:
            result = {
                'message': 'Login credentials are required.'
            }
            return make_response(jsonify(result),400) #jasonify will convert the dict into jason object
        
        email = login_credentials.get('email', None)
        password = login_credentials.get('password', None)

        if not email or not password:
            result = {
                'message': 'Email and Password are required.'
            }
            return make_response(jsonify(result),400)
        
        user = user_datastore.find_user(email=email)
        if not user:
            result = {
                'message': 'User not found.'
            }
            return make_response(jsonify(result),400)
        
        if not utils.verify_password(password, user.password): # for encrypted password, is password!=enc, simply password == user.password
            result = {
                'message': 'Invalid password.'
            }
            return make_response(jsonify(result),400)
        
        auth_token = user.get_auth_token() #from Usermixin class, get_auth_token func is inherited

        utils.login_user(user) #which user is currently logged in

        response = {
            'message': 'Login successful.',
            'user_details' : {
                'email' : user.email,
                'full_name' : user.full_name,
                'phone_number' : user.phone_number,
                'roles' : [role.name for role in user.roles ],
                'auth_token' : auth_token
            }
        }

        return make_response(jsonify(response), 200)
    
class LogoutAPI(Resource):
    @auth_token_required
    def post(self):
        utils.logout_user()

        response = {
            'message': 'Logout successful'
        }

        return make_response(jsonify(response), 200)
    
class RegisterAPI(Resource):
    def post(self):
        creds = request.get_json()

        if not creds:
            result = {
                'message': 'Registration credentials are required.'
            }
            return make_response(jsonify(result), 400)
        
        full_name = creds.get('full_name', None)
        email = creds.get('email', None)
        phone_number = creds.get('phone_number', None)
        password = creds.get('password', None) 
        confirm_password = creds.get('confirm_password', None)

        if not full_name or not email or not phone_number or not password:
            result = {
                'message': 'All fields are required.'
            }
            return make_response(jsonify(result), 400)
        
        if password != confirm_password:
            result = {
                'message': 'Passwords do not match.'
            }
            return make_response(jsonify(result), 400)
        
        if len(password)<6:
            result = {
                'message': 'Password must be atleast 6 characters long.'
            }
            return make_response(jsonify(result), 400)
        
        if len(phone_number)<10 or len(phone_number)>10:
            result = {
                'message': 'Invalid Phone number.'
            }
            return make_response(jsonify(result), 400)
        
        if '@' not in email or '.' not in email.split('@')[-1]:
            result = {
                'message': 'Invalid email format.'
            }
            return make_response(jsonify(result), 400)

        
        
        if user_datastore.find_user(email = email):
            result={
                'message': 'User already exists.'
            }
            return make_response(jsonify(result), 400)
        
        user_role = user_datastore.find_role('user')

        user_datastore.create_user(
            full_name = full_name,
            email = email,
            phone_number = phone_number,
            password = password,
            roles = [user_role]
        )

        db.session.commit()
        response = {
            'message': 'Registration successful.',
            'user_details' : {
                'email' : email,
                #'full_name' : user.full_name,
                #'phone_number' : user.phone_number,
                'roles' : [user_role.name],
                #'auth_token' : auth_token
            }
        }

        return make_response(jsonify(response), 200)

        



        
