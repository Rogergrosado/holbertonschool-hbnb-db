#!/bin/bash

# Set up environment variables
export DATABASE_TYPE=postgresql
export DATABASE_URL=postgresql://user:password@localhost/hbnb_prod
export ENV=production

# Initialize the database
psql -U user -d hbnb_prod -f db.sql

# Run the application
python manage.py run

