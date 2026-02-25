#!/bin/bash
echo "Starting deployment..."

# Pull latest code
echo "Pulling latest code from GitHub..."
git pull origin main

# Pull latest Docker images
echo "Pulling Docker images..."
docker compose pull

# Stop old containers
echo "Stopping old containers..."
docker compose down

# Build new images
echo "Building new images..."
docker compose build

# Start new containers
echo "Starting new containers..."
docker compose up -d

# Run migrations
echo "Running database migrations..."
docker compose exec -T web python manage.py migrate

# Collect static files
echo "Collecting static files..."
docker compose exec -T web python manage.py collectstatic --noinput

# Show status
echo "Deployment complete!"
docker compose ps

echo "Application is running at http://your-domain.com"
