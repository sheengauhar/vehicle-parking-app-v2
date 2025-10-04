from flask import Flask
from controllers.create_database_instance import create_tables
from controllers.database import db
from controllers.config import Config
#NEW#
from controllers.user_datastore import user_datastore
#NEW# 
from flask_security import Security
from flask_restful import Api



def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    security = Security(app, user_datastore)

    api = Api(app, prefix='/api')

    app.app_context().push()

    return app,api
    
app, api = create_app()

from controllers.general_routes import *

from controllers.authentication_apis import LoginAPI, LogoutAPI, RegisterAPI
api.add_resource(LoginAPI, '/login') #endpoint
api.add_resource(LogoutAPI, '/logout')
api.add_resource(RegisterAPI, '/register')


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
