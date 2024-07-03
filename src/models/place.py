from src.models.base import Base
from src.models.city import City
from src.models.user import User
from sqlalchemy import Column, String, Text, Float, ForeignKey, Integer
from datetime import datetime
from src import db
from flask_jwt_extended import get_jwt_identity


class Place(Base):
    
    __tablename__ = 'places'
    """
    Place model:
    Represents a place or property with various attributes and relationships.
    """

    # Define the table columns
    id = db.Column(db.String(36), primary_key=True)  # Primary key
    name = db.Column(db.String(100), nullable=False)  # Name of the place
    description = db.Column(db.Text, nullable=True)  # Description of the place
    address = db.Column(db.String(255), nullable=False)  # Address of the place
    latitude = db.Column(db.Float, nullable=False)  # Latitude for location
    longitude = db.Column(db.Float, nullable=False)  # Longitude for location
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)  # Foreign key to Host
    city_id = db.Column(db.String(36), db.ForeignKey('cities.id'), nullable=False)  # Foreign key to City
    price_per_night = db.Column(db.Integer, nullable=False)  # Price per night
    number_of_rooms = db.Column(db.Integer, nullable=False)  # Number of rooms
    number_of_bathrooms = db.Column(db.Integer, nullable=False)  # Number of bathrooms
    max_guests = db.Column(db.Integer, nullable=False)  # Maximum number of guests

    def __init__(self, data: dict | None = None, **kw) -> None:
        """
        Initialize a Place instance.

        :param data: Dictionary containing place data
        :param kw: Additional keyword arguments
        """
        super().__init__(**kw)

        if not data:
            return

        # Initialize the attributes with data from the dictionary
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.address = data.get("address", "")
        self.city_id = data["city_id"]
        self.latitude = float(data.get("latitude", 0.0))
        self.longitude = float(data.get("longitude", 0.0))
        self.user_id = data["user_id"]
        self.price_per_night = int(data.get("price_per_night", 0))
        self.number_of_rooms = int(data.get("number_of_rooms", 0))
        self.number_of_bathrooms = int(data.get("number_of_bathrooms", 0))
        self.max_guests = int(data.get("max_guests", 0))

    def __repr__(self) -> str:
        """
        Return a string representation of the Place instance.

        :return: String representation of the Place
        """
        return f"<Place {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """
        Convert the Place instance to a dictionary.

        :return: Dictionary representation of the Place
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "city_id": self.city_id,
            "user_id": self.user_id,
            "price_per_night": self.price_per_night,
            "number_of_rooms": self.number_of_rooms,
            "number_of_bathrooms": self.number_of_bathrooms,
            "max_guests": self.max_guests,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def get_current_user_id():
        """
        Get the current user's ID from JWT.

        :return: Current user's ID
        """
        return get_jwt_identity().get('id')

    @staticmethod
    def create(data: dict) -> "Place":
        """
        Create a new Place instance and save it to the database.

        :param data: Dictionary containing place data
        :return: Newly created Place instance
        :raises ValueError: If the host or city is not found
        """
        from src.persistence import db

        user: User | None = User.get(data["user_id"])

        if not user:
            raise ValueError(f"User with ID {data['user_id']} not found")

        city: City | None = City.get(data["city_id"])

        if not city:
            raise ValueError(f"City with ID {data['city_id']} not found")

        new_place = Place(data=data)

        db.save(new_place)

        return new_place

    @staticmethod
    def update(place_id: str, data: dict) -> "Place | None":
        """
        Update an existing Place instance with new data.

        :param place_id: ID of the Place to update
        :param data: Dictionary containing updated data
        :return: Updated Place instance or None if not found
        """
        from src.persistence import db

        place: Place | None = Place.get(place_id)

        if not place:
            return None

        # Update place attributes with new data
        for key, value in data.items():
            setattr(place, key, value)

        db.update(place)

        return place
    
    @classmethod
    def get(cls, place_id: str) -> "Place | None":
        """
        Get a Place instance by ID.

        :param place_id: ID of the Place
        :return: Place instance or None if not found
        """
        from src.persistence import db

        return db.get(cls.__name__.lower(), place_id)

    @classmethod
    def get_all(cls) -> list["Place"]:
        """
        Get all Place instances.

        :return: List of all Place instances
        """
        from src.persistence import db

        return db.get_all(cls.__name__.lower())

    @classmethod
    def delete(cls, place_id: str) -> bool:
        """
        Delete a Place instance by ID.

        :param place_id: ID of the Place
        :return: True if the Place was deleted, False otherwise
        """
        from src.persistence import db

        place = cls.get(place_id)
        if not place:
            return False

        return db.delete(place)
