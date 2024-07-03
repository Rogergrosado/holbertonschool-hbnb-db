from datetime import datetime
import json
import os
from sqlalchemy.orm import Session
from src.models.base import Base
from src.persistence.repository import Repository
from utils.constants import FILE_STORAGE_FILENAME

from src.models.amenity import Amenity, PlaceAmenity
from src.models.city import City
from src.models.country import Country
from src.models.place import Place
from src.models.review import Review
from src.models.user import User

class DataManager(Repository):
    """
    A flexible data management class that supports both file-based and database storage.

    This class provides methods for CRUD operations (Create, Read, Update, Delete) on data objects.
    It can switch between file-based storage and database storage based on an environment variable.

    Attributes:
        __filename (str): The filename for file-based storage.
        __data (dict): A dictionary to store data in memory for file-based operations.
        use_database (bool): Flag to determine whether to use database or file-based storage.
        db_session (Session): SQLAlchemy database session for database operations.

    Usage:
        Set the USE_DATABASE environment variable to 'true' for database storage, or 'false' for file-based storage.
        Example:
            os.environ['USE_DATABASE'] = 'true'
            data_manager = DataManager(db_session)
    """

    __filename = FILE_STORAGE_FILENAME
    __data: dict[str, list] = {
        "country": [],
        "user": [],
        "amenity": [],
        "city": [],
        "review": [],
        "place": [],
        "placeamenity": [],
    }

    models = {
        "amenity": Amenity,
        "city": City,
        "country": Country,
        "place": Place,
        "placeamenity": PlaceAmenity,
        "review": Review,
        "user": User,
    }

    def __init__(self, db_session: Session = None) -> None:
        """
        Initialize the DataManager.

        Args:
            db_session (Session, optional): SQLAlchemy database session for database operations.
        """
        self.use_database = os.getenv('USE_DATABASE', 'false').lower() == 'true'
        self.db_session = db_session
        if not self.use_database:
            self.reload()

    def _save_to_file(self):
        """
        Save the current data to a file in JSON format.
        This method is used for file-based storage.
        """
        serialized = {
            k: [v.to_dict() for v in l if isinstance(v, Base)]
            for k, l in self.__data.items()
        }

        with open(self.__filename, "w") as file:
            json.dump(serialized, file)

    def get_all(self, model_name: str):
        """
        Retrieve all objects of a specific model.

        Args:
            model_name (str): The name of the model to retrieve.

        Returns:
            list: A list of all objects of the specified model.
        """
        if self.use_database:
            return self.db_session.query(self.models[model_name]).all()
        else:
            return self.__data.get(model_name, [])

    def get(self, model_name: str, obj_id: str):
        """
        Get an object by its ID.

        Args:
            model_name (str): The name of the model.
            obj_id (str): The ID of the object to retrieve.

        Returns:
            Base: The object with the specified ID, or None if not found.
        """
        if self.use_database:
            return self.db_session.query(self.models[model_name]).get(obj_id)
        else:
            for obj in self.get_all(model_name):
                if obj.id == obj_id:
                    return obj
        return None

    def reload(self):
        """
        Reload data from the file storage.
        This method is used for file-based storage to load data into memory.
        """
        if not self.use_database:
            file_data = {}
            try:
                with open(self.__filename, "r") as file:
                    file_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                pass

            for model, data in file_data.items():
                for item in data:
                    instance: Base = self.models[model](**item)

                    if "created_at" in item:
                        instance.created_at = datetime.fromisoformat(item["created_at"])
                    if "updated_at" in item:
                        instance.updated_at = datetime.fromisoformat(item["updated_at"])

                    self.save(data=instance, save_to_file=False)

    def save(self, data: Base, save_to_file=True):
        """
        Save an object to the storage.

        Args:
            data (Base): The object to save.
            save_to_file (bool, optional): Whether to save to file immediately (for file-based storage). Defaults to True.

        Returns:
            Base: The saved object.
        """
        if self.use_database:
            self.db_session.add(data)
            self.db_session.commit()
        else:
            model: str = data.__class__.__name__.lower()

            if model not in self.__data:
                self.__data[model] = []

            self.__data[model].append(data)

            if save_to_file:
                self._save_to_file()
        return data

    def update(self, obj: Base):
        """
        Update an existing object in the storage.

        Args:
            obj (Base): The object to update.

        Returns:
            Base: The updated object, or None if the object was not found.
        """
        if self.use_database:
            self.db_session.merge(obj)
            self.db_session.commit()
            return obj
        else:
            cls = obj.__class__.__name__.lower()

            for i, o in enumerate(self.__data[cls]):
                if o.id == obj.id:
                    obj.updated_at = datetime.now()
                    self.__data[cls][i] = obj
                    self._save_to_file()
                    return obj

        return None

    def delete(self, obj: Base):
        """
        Delete an object from the storage.

        Args:
            obj (Base): The object to delete.

        Returns:
            bool: True if the object was deleted, False otherwise.
        """
        if self.use_database:
            self.db_session.delete(obj)
            self.db_session.commit()
            return True
        else:
            class_name = obj.__class__.__name__.lower()

            if obj not in self.__data[class_name]:
                return False

            self.__data[class_name].remove(obj)

            self._save_to_file()

            return True
