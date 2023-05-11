AIRBNB CLONE PROJECT

A project done in a team of two:
Johnson Oragui <3xsaint@gmail.com>
Henry Agalik <agalikhenry@gmail.com>

DESCRIPTION:
AIRBnB is a complete web application,
integrating database storage, a back-end API,
and front-end interfacing in a clone of AirBnB.

The console
create my data model
manage (create, update, destroy, etc) objects via a console / command interpreter
store and persist objects to a file (JSON file)
The first piece is to manipulate a powerful storage system.
This storage engine will give us an abstraction between “My object” 
and “How they are stored and persisted”.

Web static
learn HTML/CSS
create the HTML of your application
create template of each object

MySQL storage
replace the file storage by a Database storage
map your models to a table in database by using an O.R.M.

Web framework - templating
create your first web server in Python
make your static HTML file dynamic by using objects stored in a file or database

RESTful API
expose all your objects stored via a JSON web interface
manipulate your objects via a RESTful API

Web dynamic
learn JQuery
load objects from the client side by using your own RESTful API

Storage
Persistency is really important for a web application. It means: every time your program is executed, it starts with all objects previously created from another execution. Without persistency, all the work done in a previous execution won’t be saved and will be gone.

In this project, you will manipulate 2 types of storage: file and database. For the moment, you will focus on file.

Why separate “storage management” from “model”? It’s to make your models modular and independent. With this architecture, you can easily replace your storage system without re-coding everything everywhere.

You will always use class attributes for any object. Why not instance attributes? For 3 reasons:

Provide easy class description: everybody will be able to see quickly what a model should contain (which attributes, etc…)
Provide default value of any attribute
In the future, provide the same model behavior for file storage or database storage

File storage == JSON serialization
For this first step, you have to write in a file all your objects/instances created/updated in your command interpreter and restore them when you start it. You can’t store and restore a Python instance of a class as “Bytes”, the only way is to convert it to a serializable data structure:

convert an instance to Python built in serializable data structure (list, dict, number and string) - for us it will be the method my_instance.to_json() to retrieve a dictionary
convert this data structure to a string (JSON format, but it can be YAML, XML, CSV…) - for us it will be a my_string = JSON.dumps(my_dict)
write this string to a file on disk
And the process of deserialization?

The same but in the other way:

read a string from a file on disk
convert this string to a data structure. This string is a JSON representation, so it’s easy to convert - for us it will be a my_dict = JSON.loads(my_string)
convert this data structure to instance - for us it will be a my_instance = MyObject(my_dict)

datetime
datetime is a Python module to manipulate date, time etc…

In this example, you create an instance of datetime with the current date and time:

from datetime import datetime

date_now = datetime.now()
print(type(date_now)) # <class 'datetime.datetime'>
print(date_now) # 2017-06-08 20:42:42.170922
date_now is an object, so you can manipulate it:

from datetime import timedelta

date_tomorrow = date_now + timedelta(days=1)
print(date_tomorrow) # 2017-06-09 20:42:42.170922
… you can also store it:

a_dict = { 'my_date': date_now }
print(type(a_dict['my_date'])) # <class 'datetime.datetime'>
print(a_dict) # {'my_date': datetime.datetime(2017, 6, 8, 20, 42, 42, 170922)}
What? What’s this format when a datetime instance is in a datastructure??? It’s unreadable.

How to make it readable: strftime

print(date_now.strftime("%A")) # Thursday
print(date_now.strftime("%A %d %B %Y at %H:%M:%S")) # Thursday 08 June 2017 at 20:42:42
