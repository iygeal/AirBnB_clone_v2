#!/usr/bin/python3
""" Fabric script """
from fabric.api import env, put, run, local
from datetime import datetime
import os

env.hosts = ['100.26.216.116', '3.84.161.102']


def do_pack():
    """ Generates a .tgz file from the contents of 'web_static' folder"""
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    archive_path = 'versions/web_static_{}.tgz'.format(now)
    result = local('tar -czvf {} ./web_static/'.format(archive_path))
    if result.succeeded:
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """ distributes an archive to the servers """
    if not os.path.exists(archive_path):
        return False

    file_name = os.path.basename(archive_path).split('.')[0]
    dest_dir = '/data/web_static/releases/'
    dest_file = dest_dir + file_name

    try:
        put(archive_path, '/tmp')
        run('sudo mkdir -p {}'.format(dest_file))
        run('sudo tar -xzf /tmp/{}.tgz -C {}'.format(file_name, dest_file))
        run('sudo rm -f /tmp/{}.tgz'.format(file_name))
        run('sudo mv {}/web_static/* {}/'.format(dest_file, dest_file))
        run('sudo rm -rf {}/web_static/*'.format(dest_file))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(dest_file))
        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed:", e)
        return False
