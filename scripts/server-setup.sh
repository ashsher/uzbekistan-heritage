#!/bin/bash
echo "Setting up server for Uzbekistan Heritage..."

# Update system
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
echo "Installing Docker Compose..."
sudo apt install -y docker-compose-plugin

# Install other essentials
echo "Installing essential tools..."
sudo apt install -y git curl ufw

# Configure firewall
echo "Configuring firewall..."
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw --force enable

# Verify installations
echo "Verifying installations..."
docker --version
docker compose version
git --version

echo "Server setup complete!"
echo "IMPORTANT: Log out and log back in for Docker permissions to take effect!"
