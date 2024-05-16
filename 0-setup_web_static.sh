#!/usr/bin/env bash
# Set up web servers for deployment of static webpage

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null
then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing
sudo echo "<html><head><title>Test Page</title></head><body><h1>Iygeal, testing page...</h1></body></html>" | sudo tee /data/web_static/releases/test/index.html

# Remove symbolic link if exists and create a new one
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
nginx_config="/etc/nginx/sites-available/default"

# Backup the original configuration
sudo cp $nginx_config ${nginx_config}.bak

# Update Nginx configuration with alias
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' $nginx_config

# Restart Nginx
sudo service nginx restart
