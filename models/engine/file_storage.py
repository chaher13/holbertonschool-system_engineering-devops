#!/usr/bin/python3
import json
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return self.__objects

    def new(self, obj):
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        serialized_objects = {}
        for key, obj in self.__objects.items():
            serialized_objects[key] = obj.to_dict()

        with open(self.__file_path, 'w') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        class_mapping = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Review": Review,
    }

        try:
            with open(self.__file_path, 'r') as file:
                obj_dict = json.load(file)
                for key, obj_attr in obj_dict.items():
                    class_name, obj_id = key.split('.')
                    obj_attr["__class__"] = class_name
                    if class_name in class_mapping:
                        class_obj = class_mapping[class_name]
                        obj = class_obj(**obj_attr)
                        self.__objects[key] = obj
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass
