from dotenv import load_dotenv
load_dotenv()
import os
from flask_migrate import Migrate
from flask import Flask
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask import request, make_response, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

""" app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' """
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY') 

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = (
    os.environ.get("MAIL_DEFAULT_SENDER_NAME"),
    os.environ.get("MAIL_DEFAULT_SENDER_EMAIL")
)

db = SQLAlchemy()

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)

db.init_app(app)


SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)


# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    }
)
app.register_blueprint(swaggerui_blueprint)





