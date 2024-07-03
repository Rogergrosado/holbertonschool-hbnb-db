from datetime import datetime
from src.persistence.repository import Repository
from utils.populate import populate_db
from src.models.base import Base

class MemoryRepository(Repository):
    """
    In-memory repository implementation for storing and managing data in memory.
    This class provides methods to get, save, update, and delete objects, as well as
    reload the in-memory database with initial data.
    """

    # Dictionary to hold lists of objects for each model type
    __data: dict[str, list] = {
        "country": [],
        "user": [],
        "amenity": [],
        "city": [],
        "review": [],
        "place": [],
        "placeamenity": [],
    }

    def __init__(self) -> None:
        """
        Initialize the memory repository and populate it with initial data.
        """
        self.reload()

    def get_all(self, model_name: str) -> list:
        """
        Get all objects of a given model.

        Parameters:
        model_name (str): The name of the model to retrieve objects from.

        Returns:
        list: A list of all objects of the specified model.
        """
        return self.__data.get(model_name, [])

    def get(self, model_name: str, obj_id: str):
        """
        Get an object by its ID.

        Parameters:
        model_name (str): The name of the model.
        obj_id (str): The ID of the object to retrieve.

        Returns:
        The object if found, otherwise None.
        """
        # Iterate through the list of objects for the given model
        for obj in self.get_all(model_name):
            # Return the object if the ID matches
            if obj.id == obj_id:
                return obj
        return None

    def reload(self):
        """
        Reload the in-memory database with initial data.
        """
        populate_db(self)

    def save(self, obj: Base):
        """
        Save an object to the in-memory database.

        Parameters:
        obj (Base): The object to save.

        Returns:
        The saved object.
        """
        # Get the model name from the object's class name
        cls = obj.__class__.__name__.lower()

        # Add the object to the list if it is not already present
        if obj not in self.__data[cls]:
            self.__data[cls].append(obj)

        return obj

    def update(self, obj: Base):
        """
        Update an object in the in-memory database.

        Parameters:
        obj (Base): The object to update.

        Returns:
        The updated object if successful, otherwise None.
        """
        # Get the model name from the object's class name
        cls = obj.__class__.__name__.lower()

        # Iterate through the list of objects for the given model
        for i, o in enumerate(self.__data[cls]):
            # Update the object if the ID matches
            if o.id == obj.id:
                obj.updated_at = datetime.now()
                self.__data[cls][i] = obj
                return obj

        return None

    def delete(self, obj: Base) -> bool:
        """
        Delete an object from the in-memory database.

        Parameters:
        obj (Base): The object to delete.

        Returns:
        bool: True if the object was deleted successfully, otherwise False.
        """
        # Get the model name from the object's class name
        cls = obj.__class__.__name__.lower()

        # Remove the object from the list if it is present
        if obj in self.__data[cls]:
            self.__data[cls].remove(obj)
            return True

        return False
