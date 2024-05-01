#!/usr/bin/python3

class Base:
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class Sub(Base):
    sub = ""

dict = {'name': "Charis", 'colour': "Brown", 'sub': "Subclass"}
obj = Sub(**dict)

print(obj.sub)