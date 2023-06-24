"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    """
    Parse the given command-line arguments.

    Args:
        arg (str): The command-line arguments as a string.

    Returns:
        list: A list of parsed arguments.

    The function uses regular expressions to parse the arguments within curly braces ({}) or square brackets ([]),
    and splits the remaining arguments using shlex.split().
    """
    # Find curly braces and extract the content within them
    curly_braces = re.search(r"\{(.*?)\}", arg)
    # Find square brackets and extract the content within them
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            # Split the arguments using shlex.split() and remove commas
            return [i.strip(",") for i in split(arg)]
        else:
            # Split the arguments before the square brackets
            lexer = split(arg[:brackets.span()[0]])
            # Remove commas from each argument
            retl = [i.strip(",") for i in lexer]
            # Append the content within square brackets to the list
            retl.append(brackets.group())
            return retl
    else:
        # Split the arguments before the curly braces
        lexer = split(arg[:curly_braces.span()[0]])
        # Remove commas from each argument
        retl = [i.strip(",") for i in lexer]
        # Append the content within curly braces to the list
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HBNB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """
    # Set the command prompt to "(hbnb) "
    prompt = "(hbnb) "
    # Set the allowed classes as a set of class names
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        # Define a dictionary mapping command names to corresponding methods
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        # Check if the argument contains a dot (indicating a method call)
        match = re.search(r"\.", arg)

        if match is not None:
            # Split the argument into object and method parts
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            # Check if the method part contains parentheses (indicating arguments)
            match = re.search(r"\((.*?)\)", argl[1])

            if match is not None:
                # Split the method part into command and args
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]

                if command[0] in argdict.keys():
                    # Construct the full method call
                    call = "{} {}".format(argl[0], command[1])
                    # Call the corresponding method with the full method call
                    return argdict[command[0]](call)
        # Print an error message for unknown syntax
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
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        # Parse the arguments
        argl = parse(arg)

        if len(argl) == 0:
            # Print an error message if class name is missing
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            # Print an error message if class doesn't exist
            print("** class doesn't exist **")
        else:
            # Create a new instance of the specified class, print its id, and save it
            print(eval(argl[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        # Parse the arguments
        argl = parse(arg)
        # Get all objects from the data storage
        objdict = storage.all()

        if len(argl) == 0:
            # Print an error message if class name is missing
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            # Print an error message if class doesn't exist
            print("** class doesn't exist **")
        elif len(argl) == 1:
            # Print an error message if instance id is missing
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            # Print an error message if instance is not found
            print("** no instance found **")
        else:
            # Print the string representation of the specified instance
            print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        # Parse the arguments
        argl = parse(arg)
        # Get all objects from the data storage
        objdict = storage.all()
        if len(argl) == 0:
            # Print an error message if class name is missing
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            # Print an error message if class doesn't exist
            print("** class doesn't exist **")
        elif len(argl) == 1:
            # Print an error message if instance id is missing
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            # Print an error message if instance is not found
            print("** no instance found **")
        else:
            # Delete the specified instance from the data storage
            del objdict["{}.{}".format(argl[0], argl[1])]
            # Save the updated data storage
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        # Parse the arguments
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            # Print string representations of all instances
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            # If no class name is provided
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            # If the class doesn't exist
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            # If no instance ID is provided
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            # If the instance doesn't exist
            print("** no instance found **")
            return False
        if len(argl) == 2:
            # If no attribute name is provided
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                # If no value is provided
                print("** value missing **")
                return False

        if len(argl) == 4:
            # If there are four arguments provided
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                # If the attribute name exists in the class definition
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])  # Update the attribute value
            else:
                obj.__dict__[argl[2]] = argl[3]  # Add a new attribute with the provided value
        elif type(eval(argl[2])) == dict:
            # If the third argument is of type dict
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    # If the attribute name exists in the class definition and its type is valid
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)  # Update the attribute value
                else:
                    obj.__dict__[k] = v  # Add a new attribute with the provided value
        storage.save()  # Save the changes to the storage



if __name__ == "__main__":
    HBNBCommand().cmdloop()
