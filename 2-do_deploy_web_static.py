#!/usr/bin/python3
"""
Fabric script for deploying an archive to web servers
"""

from fabric.api import run, env, put
import os

# Server IPs
env.hosts = ['100.26.216.116', '3.84.161.102']
env.user = 'ubuntu'  # SSH username
# Path to SSH private key
env.key_filename = '~/.ssh/alx_rsa'

# Short variable names for paths
current_path = '/data/web_static/current'
releases_path = '/data/web_static/releases'


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    # Extract filename and folder name
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = f"{releases_path}/{folder_name}"

    try:
        # Upload archive to /tmp/ directory
        put(archive_path, f"/tmp/{file_name}")

        # Create directory for the new version
        run(f"mkdir -p {folder_path}")

        # Extract archive to the new version directory
        run(f"tar -xzf /tmp/{file_name} -C {folder_path}")

        # Remove archive from the server
        run(f"rm -rf /tmp/{file_name}")

        # Move contents of web_static folder to new version directory
        run(f"mv {folder_path}/web_static/* {folder_path}/")

        # Remove empty web_static folder
        run(f"rm -rf {folder_path}/web_static")

        # Remove current symlink
        run(f"rm -rf {current_path}")

        # Create new symlink pointing to the new version directory
        run(f"ln -s {folder_path} {current_path}")

        print('New version deployed!')
        return True
    except Exception as e:
        print("Deployment failed:", e)
        return False
