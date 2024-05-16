#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder of AirBnB Clone repo, using the function do_pack.
"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    # Create the versions folder if it doesn't exist
    if not os.path.exists("versions"):
        os.makedirs("versions")

    # Get the current date and time
    now = datetime.now()

    # Format the archive name as reequired
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)

    # Create the tgz archive
    result = local("tar -cvzf versions/{} web_static".format(archive_name))

    # Check if the archive was created successfully
    if result.succeeded:
        return "versions/{}".format(archive_name)
    else:
        return None
