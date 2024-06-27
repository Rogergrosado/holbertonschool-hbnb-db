import os
from flask.cli import FlaskGroup
from src import create_app
from SQL.init_db import db, app
from sqlalchemy_utils import database_exists, create_database

cli = FlaskGroup(create_app=create_app)

def initialize_database():
    env = os.getenv('ENV', 'development')
    if env == 'development' and not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])
        print("Development database created.")
    elif env == 'production':
        # Ensure production database exists and is initialized using db.sql
        os.system(f"psql -U user -d hbnb_prod -f SQL/db.sql")
        print("Production database initialized.")

if __name__ == "__main__":
    initialize_database()
    cli()

