# PerspectiveConnect - Production Deployment Guide

## Prerequisites

- Ubuntu 20.04 LTS or newer
- Root or sudo access
- Domain name (optional but recommended for SSL)
- At least 2GB RAM, 2 CPU cores, 20GB storage

---

## Option 1: Docker Deployment (Recommended)

### 1. Install Docker and Docker Compose

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo apt install docker-compose -y

# Verify installation
docker --version
docker-compose --version
```

### 2. Clone and Configure Project

```bash
# Clone your repository
git clone <your-repo-url> /opt/perspectiveconnect
cd /opt/perspectiveconnect

# Create production .env file
cp backend/.env.example backend/.env
nano backend/.env
```

**Edit `backend/.env` with production values:**
```env
OPENAI_API_KEY=your_production_api_key
JWT_SECRET=your_secure_random_secret_here
JWT_ALG=HS256
JWT_EXPIRE_DAYS=7

DB_HOST=mysql
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_strong_mysql_password
DB_NAME=perspectiveconnect

AUDIO_STORAGE_DIR=./app/storage
MODEL_NAME=gpt-4o
```

### 3. Update Docker Compose for Production

Create `docker-compose.prod.yml`:

```yaml
services:
  mysql:
    image: mysql:8.0
    container_name: pc_mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
      MYSQL_DATABASE: perspectiveconnect
    ports:
      - "127.0.0.1:3308:3306"  # Only localhost access
    volumes:
      - pc_mysql_data:/var/lib/mysql
    restart: always
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-p${DB_PASSWORD}"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: ./backend
    container_name: pc_backend
    env_file:
      - ./backend/.env
    environment:
      DB_HOST: mysql
      DB_PORT: 3306
      DB_USER: root
      DB_PASSWORD: ${DB_PASSWORD}
      DB_NAME: perspectiveconnect
    ports:
      - "127.0.0.1:9000:9000"  # Only localhost access
    volumes:
      - ./backend/app/storage:/app/app/storage
    depends_on:
      mysql:
        condition: service_healthy
    restart: always

  frontend:
    build: ./frontend
    container_name: pc_frontend
    environment:
      NEXT_PUBLIC_API_BASE: https://yourdomain.com/api
    ports:
      - "127.0.0.1:6000:6000"  # Only localhost access
    depends_on:
      - backend
    restart: always

volumes:
  pc_mysql_data:
```

### 4. Deploy with Docker

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d --build

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## Option 2: Manual Deployment

### 1. Install System Dependencies

```bash
sudo apt update && sudo apt upgrade -y

# Install Python and Node.js
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential
sudo apt install -y nodejs npm
sudo npm install -g n
sudo n stable  # Install latest stable Node.js

# Install FFmpeg
sudo apt install -y ffmpeg

# Install Nginx
sudo apt install -y nginx

# Install MySQL
sudo apt install -y mysql-server
sudo mysql_secure_installation
```

### 2. Setup MySQL Database

```bash
sudo mysql -u root -p

# In MySQL shell:
CREATE DATABASE perspectiveconnect;
CREATE USER 'pc_user'@'localhost' IDENTIFIED BY 'your_strong_password';
GRANT ALL PRIVILEGES ON perspectiveconnect.* TO 'pc_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Deploy Backend

```bash
# Create app directory
sudo mkdir -p /opt/perspectiveconnect
sudo chown $USER:$USER /opt/perspectiveconnect
cd /opt/perspectiveconnect

# Clone repository
git clone <your-repo-url> .

# Setup Python virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with production values

# Create storage directory
mkdir -p app/storage

# Test backend
uvicorn app.main:app --host 0.0.0.0 --port 9000
# Press Ctrl+C to stop
```

### 4. Create Backend Service (systemd)

```bash
sudo nano /etc/systemd/system/perspectiveconnect-backend.service
```

**Content:**
```ini
[Unit]
Description=PerspectiveConnect Backend API
After=network.target mysql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/perspectiveconnect/backend
Environment="PATH=/opt/perspectiveconnect/backend/venv/bin"
ExecStart=/opt/perspectiveconnect/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 9000 --workers 4
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Start the service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable perspectiveconnect-backend
sudo systemctl start perspectiveconnect-backend
sudo systemctl status perspectiveconnect-backend
```

### 5. Deploy Frontend

```bash
cd /opt/perspectiveconnect/frontend

# Install dependencies
npm install

# Build for production
npm run build

# Test production build
npm run start
# Press Ctrl+C to stop
```

### 6. Create Frontend Service (systemd)

```bash
sudo nano /etc/systemd/system/perspectiveconnect-frontend.service
```

**Content:**
```ini
[Unit]
Description=PerspectiveConnect Frontend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/perspectiveconnect/frontend
Environment="PATH=/usr/bin:/usr/local/bin"
Environment="NODE_ENV=production"
ExecStart=/usr/bin/npm run start
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

**Start the service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable perspectiveconnect-frontend
sudo systemctl start perspectiveconnect-frontend
sudo systemctl status perspectiveconnect-frontend
```

---

## Configure Nginx Reverse Proxy

### 1. Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/perspectiveconnect
```

**Content:**
```nginx
# Backend API
upstream backend {
    server 127.0.0.1:9000;
}

# Frontend
upstream frontend {
    server 127.0.0.1:6000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Backend API
    location /api/ {
        rewrite ^/api/(.*) /$1 break;
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Increase timeout for AI processing
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # File upload limit
    client_max_body_size 100M;
}
```

### 2. Enable Site

```bash
# Test configuration
sudo nginx -t

# Enable site
sudo ln -s /etc/nginx/sites-available/perspectiveconnect /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Restart Nginx
sudo systemctl restart nginx
```

---

## Setup SSL/HTTPS with Let's Encrypt

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

**Certbot will automatically update your Nginx config for HTTPS!**

---

## Security Hardening

### 1. Configure Firewall

```bash
# Install UFW
sudo apt install -y ufw

# Allow SSH (IMPORTANT: Do this first!)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
sudo ufw status
```

### 2. Secure MySQL

```bash
# Only allow local connections
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

# Ensure this line exists:
bind-address = 127.0.0.1

# Restart MySQL
sudo systemctl restart mysql
```

### 3. Regular Updates

```bash
# Create update script
sudo nano /usr/local/bin/update-perspectiveconnect.sh
```

**Content:**
```bash
#!/bin/bash
cd /opt/perspectiveconnect
git pull
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart perspectiveconnect-backend

cd /opt/perspectiveconnect/frontend
npm install
npm run build
sudo systemctl restart perspectiveconnect-frontend
```

```bash
sudo chmod +x /usr/local/bin/update-perspectiveconnect.sh
```

---

## Monitoring and Logs

### View Logs

```bash
# Backend logs
sudo journalctl -u perspectiveconnect-backend -f

# Frontend logs
sudo journalctl -u perspectiveconnect-frontend -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Docker logs (if using Docker)
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Check Service Status

```bash
sudo systemctl status perspectiveconnect-backend
sudo systemctl status perspectiveconnect-frontend
sudo systemctl status nginx
sudo systemctl status mysql
```

---

## Backup Strategy

### 1. Database Backup Script

```bash
sudo nano /usr/local/bin/backup-perspectiveconnect-db.sh
```

**Content:**
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/perspectiveconnect"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

mysqldump -u root -p'your_mysql_password' perspectiveconnect | gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete
```

```bash
sudo chmod +x /usr/local/bin/backup-perspectiveconnect-db.sh

# Add to crontab (daily at 2 AM)
sudo crontab -e
0 2 * * * /usr/local/bin/backup-perspectiveconnect-db.sh
```

### 2. Storage Backup

```bash
# Backup audio files
tar -czf /var/backups/perspectiveconnect/storage_$(date +%Y%m%d).tar.gz /opt/perspectiveconnect/backend/app/storage/
```

---

## Performance Optimization

### 1. Enable Nginx Caching

Add to Nginx config:
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;
```

### 2. Backend Worker Configuration

Adjust workers in systemd service:
```ini
ExecStart=/opt/perspectiveconnect/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 9000 --workers 4
```

### 3. MySQL Optimization

```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

# Add under [mysqld]
innodb_buffer_pool_size = 1G
max_connections = 200
```

---

## Troubleshooting

### Backend won't start
```bash
# Check logs
sudo journalctl -u perspectiveconnect-backend -n 50

# Check if port is in use
sudo netstat -tulpn | grep 9000

# Test manually
cd /opt/perspectiveconnect/backend
source venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 9000
```

### Frontend build fails
```bash
cd /opt/perspectiveconnect/frontend
rm -rf .next node_modules
npm install
npm run build
```

### Database connection issues
```bash
# Check MySQL status
sudo systemctl status mysql

# Test connection
mysql -u pc_user -p perspectiveconnect
```

---

## Update Frontend API Base URL

Before deploying frontend, update the API URL:

```bash
nano /opt/perspectiveconnect/frontend/.env.production
```

**Content:**
```env
NEXT_PUBLIC_API_BASE=https://yourdomain.com/api
```

Or update in `docker-compose.prod.yml` environment section.

---

## Quick Commands Reference

```bash
# Restart all services
sudo systemctl restart perspectiveconnect-backend
sudo systemctl restart perspectiveconnect-frontend
sudo systemctl restart nginx

# View status
sudo systemctl status perspectiveconnect-backend
sudo systemctl status perspectiveconnect-frontend

# Update application
/usr/local/bin/update-perspectiveconnect.sh

# Check disk space
df -h

# Check memory
free -h

# Monitor processes
htop
```

---

## Next Steps After Deployment

1. ✅ Test all features (register, login, practice, sessions)
2. ✅ Verify SSL certificate is working
3. ✅ Set up monitoring (optional: install Prometheus + Grafana)
4. ✅ Configure automated backups
5. ✅ Set up log rotation
6. ✅ Document your deployment for team

---

## Support

If you encounter issues:
1. Check logs first
2. Verify all services are running
3. Check firewall rules
4. Verify environment variables
5. Test database connection

**Remember:** Keep your OpenAI API key and JWT secret secure!
