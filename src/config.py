import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import sqlite3
#Part of the the Flask_SQLAlchemy configuration
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret')

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///hbnb_dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False



# Development configuration inherits from Config
class DevelopmentConfig(Config):
    DEBUG = True # Enable debug mode for development
    TESTING = True # Enable testing mode for development

    # Development-specific database URI, defaults to SQLite if not set
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///development.db")

    #Path to the default SQLite database file.
    db_file = 'holbertonschool-hbnb-db/src/persistence/SQLite_database.db'
    #(temporary name, to be updated when definitive SQLite database created)

    # Check if the database exists, and if not creates it.
    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute
        (
        '''
        CREATE TABLE IF NOT EXISTS users 
            (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE
            )
        '''
        )
        print("Database created successfully!")
        conn.commit()
        conn.close()
    else:
        print("SQLite database already exists.")


# Production configuration inherits from Config
class ProductionConfig(Config):
    # Production database URI, defaults to PostgreSQL if DATABASE_URL is set, otherwise local SQLite
    DEBUG = False
    TESTING = False 

    # Initialize PostgreSQL database when 
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost/hbnb_prod"
    )

app = Flask(__name__)
# Switch to DevelopmentConfig mode or ProductionConfig mode depending on the environment variable
app.config.from_object('config.DevelopmentConfig' if os.environ.get('ENV') == 'development' else 'config.ProductionConfig')
db = SQLAlchemy(app)
