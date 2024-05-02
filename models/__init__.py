#!/usr/bin/python3
"""This module instantiates an object of the appropriate storage class"""

import os

# Check the value of the environment variable HBNB_TYPE_STORAGE
storage_type = os.getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    # Import the DBStorage class
    from models.engine.db_storage import DBStorage

    # Create an instance of DBStorage and store it in the variable storage
    storage = DBStorage()
else:
    # Import the FileStorage class
    from models.engine.file_storage import FileStorage

    # Create an instance of FileStorage and store it in the variable storage
    storage = FileStorage()

# Execute the reload method after instantiating the storage object
storage.reload()
