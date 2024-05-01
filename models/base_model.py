#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, DateTime


Base = declarative_base()
"""This is the declaration of Base"""


class BaseModel:
    """A base class for all hbnb models"""

    # Class attributes
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())

    def __init__(self, *args, **kwargs):
        """BaseModel constructor method"""
        import models

        # Check if kwargs is not empty
        if kwargs:
            if "__class__" in kwargs.keys():
                del kwargs["__class__"]
                # Convert isoformat strings back to datetime objects
            if 'created_at' in kwargs.keys():
                kwargs["created_at"] = datetime.fromisoformat(
                    kwargs["created_at"])
            else:
                self.created_at = datetime.now()
            if 'updated_at' in kwargs.keys():
                kwargs["updated_at"] = datetime.fromisoformat(
                    kwargs["updated_at"])
            else:
                self.updated_at = datetime.now()
            if "id" not in kwargs.keys():
                self.id = str(uuid.uuid4())

            # Set other keys to their appropriate values
            for key, value in kwargs.items():
                # Check if the attribute already exists
                if not hasattr(self, key):
                    setattr(self, key, value)

        else:
            # If kwargs is empty, create new attributes
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        # models.storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        # Initialize an empty dictionary to hold the converted instance attributes
        dictionary = {}

        # Copy all instance attributes to the dictionary
        dictionary.update(self.__dict__)

        # Check if '_sa_instance_state' key exists in the dictionary
        if '_sa_instance_state' in dictionary:
            # If the key exists, remove it from the dictionary
            del dictionary['_sa_instance_state']

        # Add the '__class__' key to the dictionary with the class name as its value
        dictionary.update({'__class__':
                           (str(type(self)).split('.')[-1]).split('\'')[0]})

        # Convert 'created_at' and 'updated_at' attributes to ISO format strings and add them to the dictionary
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        return dictionary

    def delete(self):
        """Delete the current instance from the storage"""
        # Call the delete method from the storage to remove the instance
        import models
        models.storage.delete(self)
