from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
from src.config import DevelopmentConfig, ProductionConfig, TestingConfig

load_dotenv()

cors = CORS()
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(config_class=None) -> Flask:
    print("Creating app...")
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    
    env = os.getenv('ENV', 'development')

    if env == 'development':
        app.config.from_object(DevelopmentConfig)
    elif env == 'testing':
        app.config.from_object(TestingConfig)
    elif env == 'production':
        app.config.from_object(ProductionConfig)

    if config_class:
        app.config.from_object(config_class)

    # Use get method with a default value to avoid KeyError
    print(f"Using config: {app.config.get('ENV', 'undefined')}")

    register_extensions(app)
    register_routes(app)
    register_handlers(app)

    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")

    return app

def register_extensions(app: Flask) -> None:
    print("Registering extensions...")
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    with app.app_context():
        db.create_all()
    print("Extensions registered")

def register_routes(app: Flask) -> None:
    print("Registering routes...")
    from src.routes.users import users_bp
    from src.routes.countries import countries_bp
    from src.routes.cities import cities_bp
    from src.routes.places import places_bp
    from src.routes.amenities import amenities_bp
    from src.routes.reviews import reviews_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(amenities_bp)
    
    print("Routes registered")

def register_handlers(app: Flask) -> None:
    print("Registering error handlers...")
    app.register_error_handler(404, lambda e: (
        {"error": "Not found", "message": str(e)}, 404
    ))
    app.register_error_handler(400, lambda e: (
        {"error": "Bad request", "message": str(e)}, 400
    ))
    print("Error handlers registered")

