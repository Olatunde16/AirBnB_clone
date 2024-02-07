#!/usr/bin/python3
"""Defines the HBNBCommand class."""
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
    """Command interpreter for the HBnB project."""

    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program."""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty input."""
        pass

    def do_create(self, arg):
        """Create a new instance of BaseModel and save it."""
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split()
        class_name = arg_list[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        new_instance = eval(class_name)()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Prints the string representation of an instance."""
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split()
        class_name = arg_list[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        instances = storage.all()
        key = "{}.{}".format(class_name, arg_list[1])
        if key not in instances:
            print("** no instance found **")
        else:
            print(instances[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id."""
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split()
        class_name = arg_list[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        instances = storage.all()
        key = "{}.{}".format(class_name, arg_list[1])
        if key not in instances:
            print("** no instance found **")
        else:
            del instances[key]
            storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances."""
        instances = storage.all()
        if not arg:
            print([str(value) for value in instances.values()])
        else:
            arg_list = arg.split()
            class_name = arg_list[0]
            if class_name not in globals():
                print("** class doesn't exist **")
                return
            print([str(value) for key, value in instances.items() if class_name in key])

    def do_update(self, arg):
        """Updates an instance based on the class name and id."""
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split()
        class_name = arg_list[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        instances = storage.all()
        key = "{}.{}".format(class_name, arg_list[1])
        if key not in instances:
            print("** no instance found **")
            return
        if len(arg_list) < 3:
            print("** attribute name missing **")
            return
        if len(arg_list) < 4:
            print("** value missing **")
            return
        instance = instances[key]
        attribute_name = arg_list[2]
        attribute_value = arg_list[3]
        if hasattr(instance, attribute_name):
            attribute_type = type(getattr(instance, attribute_name))
            setattr(instance, attribute_name, attribute_type(attribute_value))
            instance.save()
        else:
            print("** no attribute found **")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
