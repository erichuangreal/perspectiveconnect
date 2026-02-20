# PerspectiveConnect - Quick Start Guide

> **🆕 First time deploying?** Use [FIRST-DEPLOYMENT.md](./FIRST-DEPLOYMENT.md) instead!  
> This guide is for experienced users with servers already set up.

## 🚀 Quick Production Deployment (5 minutes)

### Prerequisites
- Ubuntu 20.04+ server with sudo access
- Docker & Docker Compose already installed
- Domain name pointed to your server IP (optional)
- 2GB RAM minimum
- OpenAI API key ready

### Step-by-Step Deployment

```bash
# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
sudo apt install -y docker-compose
newgrp docker

# 2. Clone your repository
git clone <your-repo-url> /opt/perspectiveconnect
cd /opt/perspectiveconnect

# 3. Configure environment
cp .env.production.example backend/.env
nano backend/.env
# Add your OPENAI_API_KEY and change passwords

# 4. Deploy
./deploy-versioned.sh

# 5. Install and configure Nginx
sudo apt install -y nginx
sudo cp nginx.conf.example /etc/nginx/sites-available/perspectiveconnect
# Edit the file and replace 'yourdomain.com' with your actual domain
sudo nano /etc/nginx/sites-available/perspectiveconnect
sudo ln -s /etc/nginx/sites-available/perspectiveconnect /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# 6. Setup SSL (HTTPS)
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 7. Configure firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### ✅ Verify Deployment

Visit: `https://yourdomain.com`

Test the following:
- [ ] Register a new account
- [ ] Login
- [ ] Record and submit a practice session
- [ ] View dashboard with session history
- [ ] Check session details with feedback

### 📊 Monitor Services

```bash
# View running containers
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

### 🔄 Update Application

```bash
cd /opt/perspectiveconnect
git pull
./deploy-versioned.sh
```

### 🆘 Troubleshooting

**Backend not responding:**
```bash
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml restart backend
```

**Frontend not loading:**
```bash
docker-compose -f docker-compose.prod.yml logs frontend
docker-compose -f docker-compose.prod.yml restart frontend
```

**Database issues:**
```bash
docker-compose -f docker-compose.prod.yml logs mysql
docker-compose -f docker-compose.prod.yml exec mysql mysql -u root -p
```

### 📚 Full Documentation

See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete deployment guide with:
- Manual deployment (without Docker)
- Detailed Nginx configuration
- Security hardening
- Backup strategies
- Performance optimization
- Monitoring setup

---

## 💻 Development Mode

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your OpenAI API key
uvicorn app.main:app --reload --host 0.0.0.0 --port 9000

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

Visit: `http://localhost:6000`

---

## 🔑 Important Notes

1. **Keep your OpenAI API key secure** - Never commit it to git
2. **Change default passwords** in production
3. **Enable firewall** to protect your server
4. **Setup SSL** for HTTPS (required for production)
5. **Regular backups** of database and audio storage
6. **Monitor logs** for errors and issues

---

## 📞 Support

For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)
