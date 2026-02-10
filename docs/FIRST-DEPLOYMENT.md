# 🎯 PerspectiveConnect - First Time Deployment Guide

Complete step-by-step guide to deploy PerspectiveConnect to production for the first time.

**Estimated Time:** 30-45 minutes  
**Difficulty:** Beginner-friendly

---

## 📋 Prerequisites

Before starting, you need:

- ✅ Ubuntu 20.04+ server (2GB RAM, 2 CPU cores, 20GB storage minimum)
- ✅ Root or sudo access
- ✅ Domain name pointed to your server IP (optional but recommended)
- ✅ OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- ✅ SSH access to your server

---

## 🚀 Step-by-Step Deployment

### Step 1: Connect to Your Server

```bash
ssh your-username@your-server-ip
```

If this is your first time:
```bash
ssh root@your-server-ip
```

---

### Step 2: Update System & Install Docker

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group (so you don't need sudo)
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install -y docker-compose

# Apply docker group (or logout/login)
newgrp docker

# Verify installation
docker --version
docker-compose --version
```

**Expected output:**
```
Docker version 24.0.7, build ...
docker-compose version 1.29.2, build ...
```

---

### Step 3: Install Git

```bash
sudo apt install -y git
git --version
```

---

### Step 4: Clone Your Repository

```bash
# Create application directory
sudo mkdir -p /opt/perspectiveconnect
sudo chown $USER:$USER /opt/perspectiveconnect

# Clone repository
cd /opt/perspectiveconnect
git clone https://github.com/your-username/perspectiveconnect.git .

# Or if using SSH:
# git clone git@github.com:your-username/perspectiveconnect.git .

# Verify files are there
ls -la
```

**You should see:**
```
backend/
frontend/
docker-compose.yml
deploy-versioned.sh
README.md
...
```

---

### Step 5: Configure Environment Variables

```bash
# Copy example environment file
cd /opt/perspectiveconnect
cp .env.production.example backend/.env

# Edit with your production values
nano backend/.env
```

**Update these values in the file:**

```env
# REQUIRED: Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-actual-openai-api-key-here

# REQUIRED: Generate a secure secret
# Run this command to generate: openssl rand -base64 32
JWT_SECRET=your-secure-random-secret-here

# REQUIRED: Set a strong MySQL password
DB_PASSWORD=your-strong-mysql-password-here

# Leave these as default for Docker setup
MODEL_NAME=gpt-4o
DB_HOST=mysql
DB_PORT=3306
DB_USER=root
DB_NAME=perspectiveconnect
AUDIO_STORAGE_DIR=./app/storage
```

**To generate a secure JWT secret:**
```bash
openssl rand -base64 32
```

**Save and exit:** Press `Ctrl+X`, then `Y`, then `Enter`

---

### Step 6: Prepare Deployment Directories

```bash
cd /opt/perspectiveconnect

# Create versions directory for backups
sudo mkdir -p /opt/perspectiveconnect-versions
sudo chown $USER:$USER /opt/perspectiveconnect-versions

# Make all deployment scripts executable
chmod +x deploy-versioned.sh rollback.sh list-versions.sh cleanup-versions.sh
```

### Step 7: Run First Deployment

```bash
# Run first deployment
./deploy-versioned.sh
```

**What this does:**
1. ✅ Creates version backup directory
2. ✅ Pulls latest code
3. ✅ Builds Docker images (backend, frontend, MySQL)
4. ✅ Starts all services
5. ✅ Performs health checks
6. ✅ Shows deployment status

**This will take 5-10 minutes** (building images for the first time).

**Expected output:**
```
🚀 PerspectiveConnect Versioned Deployment
Version: v20260204_143022

📦 Step 1: Creating version backup...
✅ Backup created

📥 Step 2: Pulling latest code...
Already up to date.

🔧 Step 3: Building new version...
[+] Building 245.3s
✅ Build complete

🔄 Step 4: Deploying new version...
✅ Services started

⏳ Step 5: Waiting for services to be ready...
✅ Health check passed

🎉 Deployment Successful!

Version: v20260204_143022
Backend:  http://localhost:9000
Frontend: http://localhost:4000
```

---

### Step 8: Verify Services Are Running

```bash
# Check service status
docker-compose -f docker-compose.prod.yml ps
```

**Expected output:**
```
NAME            IMAGE           STATUS          PORTS
pc_backend      pc_backend      Up 2 minutes    127.0.0.1:9000->9000/tcp
pc_frontend     pc_frontend     Up 2 minutes    127.0.0.1:4000->4000/tcp
pc_mysql        mysql:8.0       Up 2 minutes    127.0.0.1:3306->3306/tcp
```

**All services should show "Up".**

```bash
# Test backend
curl http://localhost:9000/docs
# Should return HTML

# Test frontend
curl http://localhost:4000
# Should return HTML
```

---

### Step 9: Install and Configure Nginx

Nginx will act as a reverse proxy, handling external traffic and SSL.

```bash
# Install Nginx
sudo apt install -y nginx

# Copy example configuration
sudo cp /opt/perspectiveconnect/nginx.conf.example \
  /etc/nginx/sites-available/perspectiveconnect

# Edit configuration with your domain
sudo nano /etc/nginx/sites-available/perspectiveconnect
```

**Replace `yourdomain.com` with your actual domain in these lines:**
```nginx
server_name yourdomain.com www.yourdomain.com;
```

**If you don't have a domain yet**, use your server IP:
```nginx
server_name your-server-ip;
```

**Save and exit:** `Ctrl+X`, `Y`, `Enter`

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/perspectiveconnect \
  /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t
```

**Expected output:**
```
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

```bash
# Restart Nginx
sudo systemctl restart nginx

# Enable Nginx to start on boot
sudo systemctl enable nginx
```

---

### Step 9: Configure Firewall

```bash
# Install UFW (if not already installed)
sudo apt install -y ufw

# IMPORTANT: Allow SSH first (or you'll lock yourself out!)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

**Expected output:**
```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
```

---

### Step 11: Setup SSL/HTTPS (Highly Recommended)

**Skip this step if you don't have a domain name yet.**

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate (replace with your domain)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

**Follow the prompts:**
1. Enter your email address
2. Agree to Terms of Service: `Y`
3. Share email with EFF (optional): `Y` or `N`
4. Redirect HTTP to HTTPS: `2` (recommended)

**Certbot will automatically:**
- ✅ Obtain SSL certificate
- ✅ Update Nginx configuration
- ✅ Setup auto-renewal

```bash
# Test auto-renewal
sudo certbot renew --dry-run
```

**Expected output:**
```
Congratulations, all simulated renewals succeeded
```

---

### Step 11: Test Your Deployment

#### Option A: With Domain Name (and SSL)

Visit in your browser:
```
https://yourdomain.com
```

#### Option B: Without Domain (IP only)

Visit in your browser:
```
http://your-server-ip
```

**You should see the PerspectiveConnect login page!**

---

### Step 13: Create Your First Account

1. **Click "Register"**
2. **Fill in:**
   - Email: your-email@example.com
   - Username: yourusername
   - Password: (secure password)
3. **Click "Create account"**
4. **You should be redirected to the Dashboard**

---

### Step 14: Test Practice Feature

1. **Click "Practice" button**
2. **Click "Start recording"**
3. **Speak for 20-30 seconds** (test recording)
4. **Click "Stop"**
5. **Click "Submit for feedback"**
6. **Wait 30-60 seconds** for AI processing
7. **View your session with transcript and feedback!**

---

## ✅ Deployment Complete!

Congratulations! 🎉 Your PerspectiveConnect application is now live!

### What You've Accomplished:

- ✅ Server setup with Docker
- ✅ Application deployed with versioning
- ✅ MySQL database running
- ✅ Nginx reverse proxy configured
- ✅ Firewall enabled for security
- ✅ SSL/HTTPS configured (if domain available)
- ✅ Application tested and working

---

## 📊 Post-Deployment Tasks

### Monitor Your Application

```bash
# View all services
docker-compose -f docker-compose.prod.yml ps

# View logs (all services)
docker-compose -f docker-compose.prod.yml logs -f

# View logs (specific service)
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend

# Exit logs: Ctrl+C
```

### Check Deployment Version

```bash
cd /opt/perspectiveconnect
./list-versions.sh
```

### Setup Database Backups (Recommended)

```bash
# Create backup script
sudo nano /usr/local/bin/backup-perspectiveconnect.sh
```

**Add this content:**
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/perspectiveconnect"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

cd /opt/perspectiveconnect
docker-compose -f docker-compose.prod.yml exec -T mysql \
  mysqldump -u root -p'your_mysql_password' perspectiveconnect | \
  gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Keep only last 7 days
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/db_backup_$DATE.sql.gz"
```

**Make it executable:**
```bash
sudo chmod +x /usr/local/bin/backup-perspectiveconnect.sh
```

**Add to crontab (daily at 2 AM):**
```bash
sudo crontab -e
```

**Add this line:**
```
0 2 * * * /usr/local/bin/backup-perspectiveconnect.sh
```

**Test backup manually:**
```bash
sudo /usr/local/bin/backup-perspectiveconnect.sh
```

---

## 🔄 Future Updates

### Deploy New Versions

```bash
cd /opt/perspectiveconnect
git pull origin main  # or your branch name
./deploy-versioned.sh
```

### Rollback if Needed

```bash
./rollback.sh
```

### View Deployment History

```bash
./list-versions.sh
```

---

## 🔍 Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs

# Check if ports are available
sudo netstat -tulpn | grep -E '4000|9000|3306'

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

### Can't Connect to Application

```bash
# Check Nginx
sudo systemctl status nginx
sudo nginx -t

# Check firewall
sudo ufw status

# Test locally
curl http://localhost:9000/docs
curl http://localhost:4000
```

### Database Connection Error

```bash
# Check MySQL is running
docker-compose -f docker-compose.prod.yml ps mysql

# Check MySQL logs
docker-compose -f docker-compose.prod.yml logs mysql

# Verify password in .env matches docker-compose.prod.yml
```

### OpenAI API Errors

```bash
# Verify API key in backend/.env
nano backend/.env

# Check backend logs for errors
docker-compose -f docker-compose.prod.yml logs backend | grep -i openai

# Restart backend after fixing
docker-compose -f docker-compose.prod.yml restart backend
```

---

## 📚 Next Steps

1. **Read the documentation:**
   - [VERSIONING.md](./VERSIONING.md) - Learn about version management
   - [DEPLOYMENT-CHEATSHEET.md](./DEPLOYMENT-CHEATSHEET.md) - Quick command reference
   - [DEPLOYMENT.md](./DEPLOYMENT.md) - Advanced deployment options

2. **Setup monitoring** (optional):
   - Install monitoring tools (Prometheus, Grafana)
   - Setup log aggregation

3. **Configure automated backups**:
   - Database backups
   - Audio storage backups

4. **Setup CI/CD** (optional):
   - Automated testing
   - Automated deployments

---

## 🆘 Need Help?

### Common Issues

**"Permission denied" errors:**
```bash
sudo chown -R $USER:$USER /opt/perspectiveconnect
```

**Docker: "Cannot connect to Docker daemon":**
```bash
sudo systemctl start docker
sudo usermod -aG docker $USER
newgrp docker
```

**Nginx: "Address already in use":**
```bash
# Check what's using port 80
sudo netstat -tulpn | grep :80
# Stop conflicting service
sudo systemctl stop apache2  # if Apache is running
```

### Check Status Commands

```bash
# All services
docker-compose -f docker-compose.prod.yml ps

# Nginx
sudo systemctl status nginx

# Firewall
sudo ufw status

# Disk space
df -h

# Memory
free -h
```

---

## 🎓 You're All Set!

Your PerspectiveConnect application is now:
- ✅ Running in production
- ✅ Secure with firewall and SSL
- ✅ Using versioned deployments
- ✅ Ready for users
- ✅ Ready for updates

**Enjoy your AI-powered presentation trainer!** 🎤✨

---

## 📞 Quick Links

- **Main README**: [README.md](./README.md)
- **Version Management**: [VERSIONING.md](./VERSIONING.md)
- **Quick Commands**: [DEPLOYMENT-CHEATSHEET.md](./DEPLOYMENT-CHEATSHEET.md)
- **Full Deployment Guide**: [DEPLOYMENT.md](./DEPLOYMENT.md)
