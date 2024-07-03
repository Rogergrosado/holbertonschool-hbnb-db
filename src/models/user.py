from src.models.base import Base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
from datetime import datetime
from src import db, bcrypt


class User(Base):
    
    __tablename__='users'
    
    id = db.Column(db.String(36), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())


    def __init__(self, email: str, first_name: str, last_name: str, password: str, is_admin: bool = False, **kw):
        super().__init__(**kw)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.set_password(password)

    def __repr__(self) -> str:
        return f"<User {self.id} ({self.email})>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def set_password(self, password: str):
        """Set password method"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Check password method"""
        return bcrypt.check_password_hash(self.password, password)
    
    @staticmethod
    def create(user: dict) -> "User":
        from src.persistence import db

        users: list["User"] = User.get_all()

        for u in users:
            if u.email == user["email"]:
                raise ValueError("User already exists")

        new_user = User(**user)

        db.save(new_user)

        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        from src.persistence import db

        user: User | None = User.get(user_id)

        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        db.update(user)

        return user
