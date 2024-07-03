from src.models.base import Base
from src.persistence.repository import Repository
from src import db
from sqlalchemy.orm.exc import NoResultFound
from src.models import User

class DBRepository(Repository):
    """Database repository implementation"""

    def reload(self) -> None:
        """Reload data to the repository"""
        # This method is not typically needed for database repositories
        pass

    def get_all(self, model_name: str) -> list:
        """Get all objects of a model"""
        model_class = Base._decl_class_registry.get(model_name.capitalize())
        if model_class:
            return model_class.query.all()
        return []

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Get an object by id"""
        model_class = Base._decl_class_registry.get(model_name.capitalize())
        if model_class:
            return model_class.query.get(obj_id)
        return None

    def save(self, obj: Base) -> None:
        """Save an object"""
        db.session.add(obj)
        db.session.commit()

    def update(self, obj: Base) -> None:
        """Update an object"""
        db.session.commit()

    def delete(self, obj: Base) -> bool:
        """Delete an object"""
        db.session.delete(obj)
        db.session.commit()
        return True
    
    def get_by_email(self, email: str) -> Base | None:
        """Get a user object by email"""
        try:
            return User.query.filter_by(email=email).one()
        except NoResultFound:
            return None
