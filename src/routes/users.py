from flask import Blueprint, request, jsonify
from src.controllers.users import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from src.models.user import User
from src import bcrypt
from functools import wraps
from src.persistence.db import DBRepository

# Initialize the DBRepository as 'db'
db = DBRepository()

# Custom decorator to check user permissions
def check_user_permission(func):
    @wraps(func)
    @jwt_required()
    def decorated_function(user_id, *args, **kwargs):
        current_user_id = get_jwt_identity()
        user = db.get('user', user_id)  # Assuming db.get() retrieves user by ID

        if not user:
            return jsonify({"msg": "User not found"}), 404

        if current_user_id != user.id:
            return jsonify({"msg": "Unauthorized"}), 401

        return func(user_id, *args, **kwargs)

    return decorated_function

# Decorator to check admin permission
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if not claims.get("is_admin"):
                return jsonify(msg="Admins only!"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

# Create a Blueprint for the users module
users_bp = Blueprint("users", __name__, url_prefix="/users")

# Define routes for the users endpoint
users_bp.route("/", methods=["GET"])(get_users)  # Route to get all users
users_bp.route("/", methods=["POST"])(create_user)  # Route to create a new user

users_bp.route("/<user_id>", methods=["GET"])(get_user_by_id)  # Route to get a user by ID
users_bp.route("/<user_id>", methods=["PUT"])(jwt_required()(check_user_permission(update_user)))  # Route to update a user by ID with permission check
users_bp.route("/<user_id>", methods=["DELETE"])(jwt_required()(check_user_permission(delete_user)))  # Route to delete a user by ID with permission check

@users_bp.route('/login', methods=['POST'])
def login():
    print("Login attempt:", request.json)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id, additional_claims={"is_admin": user.is_admin})
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@users_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200

@users_bp.route('/admin', methods=['GET'])
@admin_required()
def admin_only():
    return jsonify(message="Welcome, admin!"), 200

@users_bp.route('/admin/endpoint', methods=['GET'])
@jwt_required()
def admin_endpoint():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return jsonify({"msg": "Forbidden"}), 403
    return jsonify({"msg": "Welcome Admin"}), 200
