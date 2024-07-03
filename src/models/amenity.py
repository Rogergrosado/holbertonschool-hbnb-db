from src.models.base import Base
from flask_sqlalchemy import SQLAlchemy
from src import db
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from datetime import datetime

class Amenity(Base):

    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    name = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, name: str, **kw) -> None:
        super().__init__(**kw)

        self.name = name

    def __repr__(self) -> str:
        return f"<Amenity {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "Amenity":
        from src.persistence import db

        amenity = Amenity(**data)

        db.save(amenity)

        return amenity

    @staticmethod
    def update(amenity_id: str, data: dict) -> "Amenity | None":
        from src.persistence import db

        amenity: Amenity | None = Amenity.get(amenity_id)

        if not amenity:
            return None

        if "name" in data:
            amenity.name = data["name"]

        db.update(amenity)

        return amenity


class PlaceAmenity(Base):
  
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    amenity_id = db.Column(db.String(36), db.ForeignKey('amenities.id'), nullable=False)

    def __init__(self, place_id: str, amenity_id: str, **kw) -> None:
        super().__init__(**kw)

        self.place_id = place_id
        self.amenity_id = amenity_id

    def __repr__(self) -> str:
        return f"<PlaceAmenity {self.id} ({self.place_id} - {self.amenity_id})>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "place_id": self.place_id,
            "amenity_id": self.amenity_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def get(place_id: str, amenity_id: str) -> "PlaceAmenity | None":  # type: ignore
        from src.persistence import db

        place_amenities: list[PlaceAmenity] = db.get_all("placeamenity")

        for place_amenity in place_amenities:
            if (
                place_amenity.place_id == place_id
                and place_amenity.amenity_id == amenity_id
            ):
                return place_amenity

        return None

    @staticmethod
    def create(data: dict) -> "PlaceAmenity":
        from src.persistence import db

        new_place_amenity = PlaceAmenity(**data)

        db.save(new_place_amenity)

        return new_place_amenity

    @staticmethod
    def delete(place_id: str, amenity_id: str) -> bool:  # type: ignore
        from src.persistence import db

        place_amenity: PlaceAmenity | None = PlaceAmenity.get(place_id, amenity_id)

        if not place_amenity:
            return False

        db.delete(place_amenity)

        return True

    @staticmethod
    def update(entity_id: str, data: dict): ...
