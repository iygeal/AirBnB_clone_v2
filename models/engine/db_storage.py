#!/usr/bin/python3
"""Module that defines db_storage engine"""

class DBStorage:
    """The database storage class"""

    # Private class attributes
    __engine = None
    __session = None

    def __init__(self):
        """Database class constructor method"""
        