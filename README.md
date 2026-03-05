# 🇺🇿 Uzbekistan Heritage

A Django web application showcasing Uzbekistan's historical periods, figures, and architectural sites. Deployed to the cloud with Docker, PostgreSQL, and automated CI/CD.

## Live Demo

**Website:** https://uzbekistan-heritage.uz  
**Admin Panel:** https://uzbekistan-heritage.uz/admin

**Test Account:**
- Username: `testuser`
- Password: `TestPass123`

**Admin Account:**
- Username: `admin`
- Password: `admin`

## Features

- User registration and authentication
- Browse historical time periods (1370-1991)
- Explore historical figures (rulers, scientists, poets, warriors)
- Discover architectural sites and monuments
- Create, edit, and delete your own entries
- Admin panel for content management
- Responsive design with purple gradient theme

## Technologies Used

**Backend:**
- Django 4.2.7
- Python 3.10
- PostgreSQL 15
- Gunicorn 21.2.0

**DevOps:**
- Docker & Docker Compose
- Nginx (Alpine)
- GitHub Actions (CI/CD)
- Let's Encrypt SSL

**Hosting:**
- Eskiz VPS 2 (Ubuntu 24.04)
- 2GB RAM, 40GB SSD

## Database Models

**TimePeriod**
- Historical eras with start/end years
- Description and images

**HistoricalFigure** (Many-to-One with TimePeriod)
- Name, biography, role
- Birth/death years
- Linked to time period

**HistoricalSite** (Many-to-Many with TimePeriod & HistoricalFigure)
- Monument name and location
- Construction year and description
- Related to multiple periods and figures

## Local Development Setup

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- Git 2.30+

### Quick Start
```bash
# Clone repository
git clone https://github.com/ashsher/uzbekistan-heritage.git
cd uzbekistan-heritage

# Create environment file
cp .env.example .env

# Start services
docker compose up -d

# Wait 30 seconds, then run migrations
docker compose exec web python manage.py migrate

# Create admin user
docker compose exec web python manage.py createsuperuser

# Access application
# Website: http://localhost
# Admin: http://localhost/admin
```

### Stop Services
```bash
docker compose down
```

## Environment Variables

Create a `.env` file with these variables:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=uzbekistan_heritage_db
DB_USER=postgres
DB_PASSWORD=your-password-here
DB_HOST=db
DB_PORT=5432
```

**Generate a secret key:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Docker Information

**Image Sizes:**
- Web Application: 79.9 MB
- PostgreSQL: 110 MB
- Nginx: 26.9 MB

**Services:**
- `db` - PostgreSQL 15 database
- `web` - Django + Gunicorn application server
- `nginx` - Nginx reverse proxy and web server

**Volumes:**
- `postgres_data` - Database persistence
- `static_volume` - Static files (CSS, JS)
- `media_volume` - User uploads

## CI/CD Pipeline

The project uses GitHub Actions for automated deployment.

**Pipeline Stages:**
1. **Test** - Run 10 automated tests + code quality checks
2. **Build** - Create Docker image and push to Docker Hub
3. **Deploy** - SSH to server, update containers, run migrations

**Triggered on:** Push to main branch  
**Deployment time:** 3-5 minutes  
**GitHub Actions:** https://github.com/ashsher/uzbekistan-heritage/actions

## Production Deployment

### Server Requirements

- Ubuntu 24.04 LTS
- 2GB RAM, 40GB storage
- Docker & Docker Compose installed
- Ports 22, 80, 443 open

### Deploy to Production
```bash
# On server
git clone https://github.com/ashsher/uzbekistan-heritage.git
cd uzbekistan-heritage

# Create production .env file
nano .env
# Add production values (DEBUG=False, production SECRET_KEY, etc.)

# Start services
docker compose up -d

# Wait 40 seconds, then run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Collect static files
docker compose exec web python manage.py collectstatic --noinput
```

### SSL Certificate Setup
```bash
# Install Certbot
apt install certbot python3-certbot-nginx

# Stop Docker
docker compose down

# Get certificate
certbot certonly --standalone -d yourdomain.uz -d www.yourdomain.uz

# Update nginx/nginx.conf with certificate paths
# Add volume mounts in docker-compose.yml
# Restart services
docker compose up -d
```

## Running Tests
```bash
# Run all tests
docker compose exec web python manage.py test

# Run with verbose output
docker compose exec web python manage.py test --verbosity=2

# Check code quality
docker compose exec web flake8 history/ uzbekistan_heritage/
```

**Test Coverage:** 10 tests (models, views, authentication)

## Project Structure
```
uzbekistan-heritage/
├── .github/workflows/    # CI/CD pipeline
├── history/              # Main Django app
│   ├── migrations/       # Database migrations
│   ├── static/           # CSS files
│   ├── templates/        # HTML templates
│   ├── models.py         # Database models
│   ├── views.py          # View logic
│   ├── forms.py          # Django forms
│   └── tests.py          # Automated tests
├── nginx/                # Nginx configuration
├── uzbekistan_heritage/  # Django project settings
├── Dockerfile            # Multi-stage Docker build
├── docker-compose.yml    # Service orchestration
├── requirements.txt      # Python dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

## Security Features

- HTTPS with Let's Encrypt SSL certificates
- UFW firewall (ports 22, 80, 443 only)
- Non-root Docker container user
- Environment-based configuration
- Security headers (HSTS, X-Frame-Options)
- DEBUG=False in production
- ALLOWED_HOSTS validation

## Screenshots

- All the screenshots are available via this project's report link:
  - https://docs.google.com/document/d/1ypkh-ZDyuwJn8bOtEuW0lvPuSe42gpIntkIXs1l6PVc/edit?usp=sharing

## Links

- **Live Website:** https://uzbekistan-heritage.uz
- **GitHub Repository:** https://github.com/ashsher/uzbekistan-heritage
- **Docker Hub:** https://hub.docker.com/r/ashsher/uzbekistan-heritage
- **CI/CD Pipeline:** https://github.com/ashsher/uzbekistan-heritage/actions

## License

This project is for educational purposes as part of university coursework

**⭐ If you find this project helpful, please star the repository!**
