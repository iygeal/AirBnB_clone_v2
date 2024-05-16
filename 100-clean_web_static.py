#!/usr/bin/python3
"""Fabric script to replicate task 3
"""

import os
from fabric.api import *

# Specify the IP addresses of the web servers
env.hosts = ['100.26.216.116', '3.84.161.102']


def do_clean(number=0):
    """
    Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    # Ensure 'number' is at least 1
    number = 1 if int(number) == 0 else int(number)

    # List and sort the local archives in the 'versions' directory
    archives = sorted(os.listdir("versions"))
    # Remove the most recent 'number' of archives from the list
    [archives.pop() for i in range(number)]
    # Delete the remaining archives locally
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    # Change to the releases directory on the remote servers
    with cd("/data/web_static/releases"):
        # List and sort the remote archives
        archives = run("ls -tr").split()
        # Filter out only the web_static archives
        archives = [a for a in archives if "web_static_" in a]
        # Remove the most recent 'number' of archives from the list
        [archives.pop() for i in range(number)]
        # Delete the remaining archives on the remote servers
        [run("rm -rf ./{}".format(a)) for a in archives]
