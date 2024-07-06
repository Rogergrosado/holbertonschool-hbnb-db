from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.controllers.reviews import (
    create_review,
    delete_review,
    get_reviews_from_place,
    get_reviews_from_user,
    get_review_by_id,
    get_reviews,
    update_review,
)

# Create a Blueprint for the reviews module
reviews_bp = Blueprint("reviews", __name__)

# Define routes for the reviews endpoint

# Route to create a new review for a place (requires JWT authentication)
reviews_bp.route("/places/<place_id>/reviews", methods=["POST"])(jwt_required()(create_review))

# Route to get all reviews for a specific place
reviews_bp.route("/places/<place_id>/reviews")(get_reviews_from_place)

# Route to get all reviews from a specific user
reviews_bp.route("/users/<user_id>/reviews")(get_reviews_from_user)

# Route to get all reviews
reviews_bp.route("/reviews", methods=["GET"])(get_reviews)

# Route to get a specific review by its ID
reviews_bp.route("/reviews/<review_id>", methods=["GET"])(get_review_by_id)

# Route to update a specific review by its ID
reviews_bp.route("/reviews/<review_id>", methods=["PUT"])(update_review)

# Route to delete a specific review by its ID
reviews_bp.route("/reviews/<review_id>", methods=["DELETE"])(delete_review)
