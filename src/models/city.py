from src.models.base import Base
from src.models.country import Country
from src import db
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref


class City(Base):
    
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country_code = db.Column(db.String(2), db.ForeignKey('countries.code'), nullable=False)
    country = db.relationship('Country', backref=db.backref('cities', lazy=True))

    def __init__(self, name: str, country_code: str, **kw) -> None:
        super().__init__(**kw)

        self.name = name
        self.country_code = country_code

    def __repr__(self) -> str:
        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "City":
        from src.persistence import db

        country = Country.get(data["country_code"])

        if not country:
            raise ValueError("Country not found")

        city = City(**data)

        db.save(city)

        return city

    @staticmethod
    def update(city_id: str, data: dict) -> "City":
        from src.persistence import db

        city = City.get(city_id)

        if not city:
            raise ValueError("City not found")

        for key, value in data.items():
            setattr(city, key, value)

        db.update(city)

        return city
