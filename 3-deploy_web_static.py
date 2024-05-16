#!/usr/bin/python3
"""
Fabric script for creating and distributing an archive to web servers
"""

from fabric.api import *
from datetime import datetime
import os

# Server IPs
env.hosts = ['100.26.216.116', '3.84.161.102']
env.user = 'ubuntu'  # SSH username
# Path to SSH private key
env.key_filename = '~/.ssh/alx_rsa'

# Variable names for paths
current_path = '/data/web_static/current'
releases_path = '/data/web_static/releases'


def do_pack():
    """
    Creates a .tgz archive from the contents of the web_static folder
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = f"versions/web_static_{now}.tgz"
    local("mkdir -p versions")
    result = local(f"tar -czvf {archive_path} web_static")
    if result.failed:
        return None
    return archive_path


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = f"{releases_path}/{folder_name}"

    try:
        put(archive_path, f"/tmp/{file_name}")
        run(f"mkdir -p {folder_path}")
        run(f"tar -xzf /tmp/{file_name} -C {folder_path}")
        run(f"rm -rf /tmp/{file_name}")
        run(f"mv {folder_path}/web_static/* {folder_path}/")
        run(f"rm -rf {folder_path}/web_static")
        run(f"rm -rf {current_path}")
        run(f"ln -s {folder_path} {current_path}")
        print('New version deployed!')
        return True
    except Exception as e:
        print("Deployment failed:", e)
        return False


def deploy():
    """
    Creates and distributes an archive to web servers
    """
    # Create archive
    archive_path = do_pack()
    if not archive_path:
        return False

    # Deploy archive
    return do_deploy(archive_path)
