# app/__init__.py
from urllib.parse import urlparse
from datetime import timedelta
import os

from flask import Flask
from flask_cors import CORS
from flask_session import Session
from flask_socketio import SocketIO
from flask_mailman import Mail

from dotenv import load_dotenv
from mongoengine import connect
from authlib.integrations.flask_client import OAuth
from openai import AsyncAzureOpenAI, AsyncOpenAI
from redis import Redis

import torch

socketio = SocketIO()
cors = CORS()
oauth = OAuth()
openai = None
device = None
mail = Mail()
app = Flask(__name__)


def create_app():
    global openai
    global device
    global app
    load_dotenv()

    # App configuration
    app.config['DEBUG'] = os.getenv('DEBUG') == 'True'

    redis_url = urlparse(os.getenv('REDIS_URI'))
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = Redis(
        host=redis_url.hostname,
        port=redis_url.port,
        password=redis_url.password
    )
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') if os.getenv('SECRET_KEY') else os.urandom(24)
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=int(os.getenv('SESSION_TIMEOUT', 604800)))
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'sess:'

    # Mail configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 465))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'false').lower() in ['true', 'on', '1']
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'true').lower() in ['true', 'on', '1']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    # OPENAI configuration and initialization
    if os.getenv('USE_AZURE_OPENAI') == 'True':
        openai = AsyncAzureOpenAI(
            azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
            api_key=os.getenv('AZURE_OPENAI_API_KEY'),
            api_version=os.getenv('AZURE_OPENAI_API_VERSION')
        )
    else:
        openai = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Here to load blueprint
    from app.routes.auth import auth_bp
    from app.routes.flash_messages import flash_message_bp
    from app.routes.index import index_bp
    from app.routes.seller.register import seller_register_bp
    from app.routes.rental.property_management import rent_property_management_bp
    from app.routes.image_viewer import image_viewer_bp
    from app.routes.rental.property_view import property_view_bp
    from app.routes.rental.find_rental import find_rental_bp
    from app.routes.api.rental.property_management import api_rent_property_management_bp as api_rent_property_management_bp

    # Here to initialize the app
    connect(host=os.getenv('MONGO_URI'))
    Session(app)
    socketio.init_app(app)
    oauth.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    if os.getenv('TORCH_DEVICE') == 'cuda':
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device("cpu")

    # Here to register blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(flash_message_bp, url_prefix='/api/v1')
    app.register_blueprint(index_bp)
    app.register_blueprint(seller_register_bp)
    app.register_blueprint(find_rental_bp, url_prefix='/rental')
    app.register_blueprint(rent_property_management_bp, url_prefix='/rental/management')
    app.register_blueprint(image_viewer_bp, url_prefix='/image')
    app.register_blueprint(property_view_bp, url_prefix='/rental')
    app.register_blueprint(api_rent_property_management_bp, url_prefix='/api/v1/rental/management')

    # Here to register sockets

    app = app
    return app
