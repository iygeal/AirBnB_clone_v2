#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel):
    """ State class """

    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete", backref="states")

    # FileStorage: getter attribute cities
    @property
    def cities(self):
        """
            Getter attribute which returns the list of City instances
            with state_id = current State.id
        """
        from models import storage
        city_list = []
        for city in storage.all("City").values():
            if city.state_id == self.id:
                city_list.append(city)
        return city_list
