from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from src import routes, models

cors = CORS()


def create_app(config_class=None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    app.url_map.strict_slashes = False

    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object("src.config.DevelopmentConfig")

    # db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

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

    @app.errorhandler(404)
    def not_found_error(error):
        return {"error": "Not found", "message": str(error)}, 404

    @app.errorhandler(400)
    def bad_request_error(error):
        return {"error": "Bad request", "message": str(error)}, 400

    return app
