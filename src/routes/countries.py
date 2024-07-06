"""
This module contains the routes for the countries endpoint
"""

from flask import Blueprint
from src.controllers.countries import (
    # create_country,
    get_countries,
    get_country_by_code,
    get_country_cities,
)

countries_bp = Blueprint("countries", __name__, url_prefix="/countries")

countries_bp.route("/", methods=["GET"])(get_countries)
countries_bp.route("/<code>", methods=["GET"])(get_country_by_code)
countries_bp.route("/<code>/cities", methods=["GET"])(get_country_cities)
# countries_bp.route("/", methods=["POST"])(create_country)

# countries_bp.route("/<country_id>", methods=["PUT"])(update_country)
# countries_bp.route("/<country_id>", methods=["DELETE"])(delete_country)
