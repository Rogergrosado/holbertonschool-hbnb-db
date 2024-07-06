from flask import jsonify
from flask import Blueprint
from src.controllers.places import (
    create_place,
    delete_place,
    get_place_by_id,
    get_places,
    update_place,
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.persistence import db
from functools import wraps


def check_place_permission(func):
    @wraps(func)
    @jwt_required()
    def decorated_function(place_id, *args, **kwargs):
        current_user = get_jwt_identity()
        place = db.get('place', place_id)

        if not place:
            return jsonify({"msg": "Place not found"}), 404

        if current_user != place.host_id:
            return jsonify({"msg": "Unauthorized"}), 401

        return func(place_id, *args, **kwargs)

    return decorated_function

places_bp = Blueprint("places", __name__, url_prefix="/places")

places_bp.route("/", methods=["GET"])(get_places)
places_bp.route("/", methods=["POST"])(jwt_required()(create_place))

places_bp.route("/<place_id>", methods=["GET"])(get_place_by_id)
places_bp.route("/<place_id>", methods=["PUT"])(jwt_required()(check_place_permission(update_place)))
places_bp.route("/<place_id>", methods=["DELETE"])(jwt_required()(check_place_permission(delete_place)))

# Example of a protected route to demonstrate JWT usage
@places_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
