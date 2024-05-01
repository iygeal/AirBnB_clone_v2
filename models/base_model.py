#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime


class BaseModel:
    """A base class for all hbnb models"""

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
                setattr(self, key, value)

            # Update object with the new parameters
            #self.__dict__.update(kwargs)

        else:
            # If kwargs is empty, create new attributes
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        models.storage.new(self)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
