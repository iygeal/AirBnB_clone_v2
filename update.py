#!/usr/bin/python3

def foo(**kwargs):
    print(kwargs)

dict = {
    'name': "Charis",
    'age': 26,
    'adict': {'col': "brown"}
}

foo(**dict)

strn = "This is a string"
first, *lis = strn.split()
print(lis)