#!/usr/bin/env python3
"""Fabric script that creates and distributes an archive to web servers"""
from fabric.api import env, local, put, run
from datetime import datetime
import os

env.hosts = ['100.26.216.116', '3.84.161.102']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/alx_rsa'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    archive_path = f'versions/web_static_{now}.tgz'

    # Create versions directory if it doesn't exist
    local('mkdir -p versions')

    # Create the archive
    result = local(f'tar -czvf {archive_path} web_static')

    # Return the archive path if successful, otherwise None
    return archive_path if result.succeeded else None


def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if not os.path.exists(archive_path):
        return False

    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace('.tgz', '')
    folder_path = f'/data/web_static/releases/{folder_name}/'

    try:
        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, f'/tmp/{file_name}')

        # Create the release folder on the server
        run(f'mkdir -p {folder_path}')

        # Uncompress the archive to the release folder
        run(f'tar -xzf /tmp/{file_name} -C {folder_path}')

        # Delete the archive from the web server
        run(f'rm -f /tmp/{file_name}')

        # Move the contents from web_static to the folder
        run(f'mv {folder_path}web_static/* {folder_path}')

        # Delete the web_static folder inside the release folder
        run(f'rm -rf {folder_path}web_static')

        # Delete the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new release
        run(f'ln -s {folder_path} /data/web_static/current')

        print("New version deployed!")
        return True
    except Exception as e:
        print(f"Deployment failed: {e}")
        return False


def deploy():
    """Creates and distributes an archive to web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
