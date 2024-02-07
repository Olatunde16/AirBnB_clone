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
        """Show an instance based on its ID."""
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split()
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        class_name = arg_list[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        instance_id = arg_list[1]
        key = "{}.{}".format(class_name, instance_id)
        instances = storage.all()
        if key in instances:
            print(instances[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Destroy an instance based on its ID."""
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split()
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        class_name = arg_list[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        instance_id = arg_list[1]
        key = "{}.{}".format(class_name, instance_id)
        instances = storage.all()
        if key in instances:
            del instances[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Prints all string representation of all instances."""
        if not arg:
            print([str(value) for value in storage.all().values()])
        else:
            arg_list = arg.split()
            class_name = arg_list[0]
            if class_name not in globals():
                print("** class doesn't exist **")
                return
            print([str(value) for value in eval(class_name).all()])

    def do_update(self, arg):
        """Update an instance based on its ID."""
        if not arg:
            print("** class name missing **")
            return
        arg_list = arg.split()
        if len(arg_list) < 2:
            print("** instance id missing **")
            return
        class_name = arg_list[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        instance_id = arg_list[1]
        key = "{}.{}".format(class_name, instance_id)
        instances = storage.all()
        if key not in instances:
            print("** no instance found **")
            return
        if len(arg_list) < 3:
            print("** dictionary missing **")
            return
        instance = instances[key]
        try:
            arg_dict = eval("{" + arg_list[2] + "}")
        except Exception:
            print("** invalid dictionary **")
            return
        for k, v in arg_dict.items():
            if hasattr(instance, k):
                attribute_type = type(getattr(instance, k))
                setattr(instance, k, attribute_type(v))
        instance.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
