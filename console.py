#!/usr/bin/python3
import cmd
from typing import IO
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import models
import shlex
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '  # Définition du prompt personnalisé

    classed = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Review": Review,
    }

    def do_quit(self, arg):
        """Quit command to exit the program
        """
        return True  # Retourne True pour indiquer la fin du programme

    def do_EOF(self, arg):
        """Handles the end of file (EOF)"""
        print()  # Affiche une nouvelle ligne pour plus de lisibilité
        return True  # Retourne True pour indiquer la fin du programme

    def emptyline(self):
        """Called when an empty line is entered"""
        pass  # Ne fait rien pour ignorer une ligne vide

    def do_create(self, arg):
        args = arg.split()
        if not args:
            print("** Class name missing **")
            return

        class_name = args[0]

        # Check if the class exists
        if class_name not in self.classed:
            print("** Class doesn't exist **")
            return

        # Create the instance, save it, and print the ID
        instance = self.classed[class_name]()
        instance.save()
        print(instance.id)

    def do_show(self, arg):
        args = arg.split()
        if not args:
            print("** Class name missing **")
            return

        if args[0] not in self.classed:
            print("** Class doesn't exist **")
            return

        if len(args) < 2:
            print("** Instance ID missing **")
            return

        storeq = args[0] + "." + args[1]
        if storeq in models.storage.all():
            print(models.storage.all()[storeq])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        args = arg.split()
        if not args:
            print("** Class name missing **")
            return

        if args[0] not in self.classed:
            print("** Class doesn't exist **")
            return

        if len(args) < 2:
            print("** Instance ID missing **")
            return

        storeq = args[0] + "." + args[1]
        if storeq in models.storage.all():
            del models.storage.all()[storeq]
            models.storage.save()
        else:
            print("** no instance found **")

    def do_update(self, arg):
        args = arg.split()
        if not args:
            print("** Class name missing **")
            return

        if args[0] not in self.classed:
            print("** Class doesn't exist **")
            return

        if len(args) < 3:
            print("** Instance ID or attribute name missing **")
            return

        storeq = args[0] + "." + args[1]
        objects = models.storage.all()
        attribute_name = args[2]
        attribute_value = args[3]
        obj = objects[storeq]

        setattr(obj, attribute_name, attribute_value)
        obj.save()

    def do_all(self, arg):
        objects = models.storage.all()

        if not arg:
            print([str(obj)for obj in objects.values()])
            return

        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.classed:
            print("** class doesn't exist **")
            return

        if class_name != "User":
            print("** class doesn't exist **")
            return

        filtered_objs = [str(obj) for obj in objects.values()
                         if isinstance(obj, self.classed[class_name])]
        print(filtered_objs)

    def do_update(self, arg):
        """Update an instance"""
        args = shlex.split(arg)
        if not args:
            print("** Class name missing **")
            return
        if args[0] not in self.classed:
            print("** Class doesn't exist **")
            return
        if len(args) < 3:
            print("** Instance ID or attribute name missing **")
            return
        storeq = args[0] + "."  + args[1]          
        objects = models.storage.all()
        attribute_name = args[2]
        attribute_value = args[3]
        obj = objects[storeq] 
        
        setattr(obj, attribute_name, attribute_value)
        obj.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
