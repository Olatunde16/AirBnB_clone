#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """Represent an abstracted storage engine."""

    def __init__(self, file_path="file.json"):
        """Initialize FileStorage with a file path."""
        self.__file_path = file_path
        self.__objects = {}

    def all(self):
        """Return the dictionary of objects."""
        return self.__objects

    def new(self, obj):
        """Add a new object to the storage."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """Serialize objects to the JSON file."""
        obj_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, "w") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserialize the JSON file to objects."""
        try:
            with open(self.__file_path) as f:
                obj_dict = json.load(f)
                for key, val in obj_dict.items():
                    cls_name = val["__class__"]
                    del val["__class__"]
                    self.new(eval(cls_name)(**val))
        except FileNotFoundError:
            return
