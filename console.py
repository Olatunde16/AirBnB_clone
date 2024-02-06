#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter."""

    prompt = "(hbnb) "
    __classes = {"BaseModel", "User", "State", "City", "Place", "Amenity", "Review"}

    def _parse_arguments(self, arg):
        """Parse the command arguments using regular expressions."""
        return re.findall(r"\w+", arg)

    def _validate_class_and_id(self, arg):
        """Validate the class name and instance ID."""
        if not arg:
            print("** class name missing **")
            return False, None
        class_name = arg.pop(0)
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return False, None
        if not arg:
            print("** instance id missing **")
            return False, None
        instance_id = arg.pop(0)
        return True, (class_name, instance_id)

    def _get_object(self, class_name, instance_id):
        """Retrieve the object from storage."""
        key = "{}.{}".format(class_name, instance_id)
        obj_dict = storage.all()
        if key not in obj_dict:
            print("** no instance found **")
            return None
        return obj_dict[key]

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        args = self._parse_arguments(arg)
        valid, instance_info = self._validate_class_and_id(args)
        if valid:
            class_name, instance_id = instance_info
            obj = self._get_object(class_name, instance_id)
            if obj:
                return False
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Create a new class instance and print its id."""
        args = self._parse_arguments(arg)
        if not args:
            print("** class name missing **")
            return
        class_name = args.pop(0)
        if class_name not in self.__classes:
            print("** class doesn't exist **")
            return
        obj = eval(class_name)()
        print(obj.id)
        storage.save()

    def do_show(self, arg):
        """Display the string representation of a class instance."""
        args = self._parse_arguments(arg)
        valid, instance_info = self._validate_class_and_id(args)
        if valid:
            class_name, instance_id = instance_info
            obj = self._get_object(class_name, instance_id)
            if obj:
                print(obj)

    def do_destroy(self, arg):
        """Delete a class instance."""
        args = self._parse_arguments(arg)
        valid, instance_info = self._validate_class_and_id(args)
        if valid:
            class_name, instance_id = instance_info
            obj = self._get_object(class_name, instance_id)
            if obj:
                del storage.all()["{}.{}".format(class_name, instance_id)]
                storage.save()

    def do_all(self, arg):
        """Display string representations of class instances."""
        args = self._parse_arguments(arg)
        class_name = args.pop(0) if args else None
        obj_list = [str(obj) for obj in storage.all().values()
                    if not class_name or obj.__class__.__name__ == class_name]
        print(obj_list)

    def do_count(self, arg):
        """Retrieve the number of instances of a given class."""
        args = self._parse_arguments(arg)
        class_name = args.pop(0) if args else None
        count = sum(1 for obj in storage.all().values()
                    if not class_name or obj.__class__.__name__ == class_name)
        print(count)

    def do_update(self, arg):
        """Update a class instance."""
        args = self._parse_arguments(arg)
        valid, instance_info = self._validate_class_and_id(args)
        if valid:
            class_name, instance_id = instance_info
            obj = self._get_object(class_name, instance_id)
            if obj:
                if len(args) < 2:
                    print("** attribute name or dictionary missing **")
                    return
                if len(args) == 2:
                    attr_name, attr_value = args
                    setattr(obj, attr_name, attr_value)
                elif len(args) == 3:
                    attr_name, attr_value = args[:2]
                    setattr(obj, attr_name, eval(attr_value))
                storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
