# 🚀 PerspectiveConnect - Deployment Cheat Sheet

Quick reference for common deployment tasks.

---

## 📦 Versioned Deployments (Recommended)

### Deploy New Version
```bash
./deploy-versioned.sh
```
- Creates timestamped backup
- Builds and deploys
- Auto-rollback on failure
- Keeps last 5 versions

### Rollback to Previous
```bash
./rollback.sh
```
- Interactive menu to select version
- Restores Docker images
- Verifies health checks

### View History
```bash
./list-versions.sh
```

### Cleanup Old Versions
```bash
./cleanup-versions.sh 3    # Keep 3 versions
```

---

## 🔧 Basic Commands

### Check Status
```bash
docker-compose -f docker-compose.prod.yml ps
```

### View Logs
```bash
docker-compose -f docker-compose.prod.yml logs -f
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
```

### Restart Services
```bash
docker-compose -f docker-compose.prod.yml restart
docker-compose -f docker-compose.prod.yml restart backend
```

### Stop Services
```bash
docker-compose -f docker-compose.prod.yml down
```

### Start Services
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🗄️ Database

### Backup Database
```bash
docker-compose -f docker-compose.prod.yml exec mysql \
  mysqldump -u root -p perspectiveconnect | gzip > backup_$(date +%Y%m%d).sql.gz
```

### Restore Database
```bash
gunzip -c backup_20260204.sql.gz | \
  docker-compose -f docker-compose.prod.yml exec -T mysql \
  mysql -u root -p perspectiveconnect
```

### Connect to Database
```bash
docker-compose -f docker-compose.prod.yml exec mysql \
  mysql -u root -p perspectiveconnect
```

---

## 🔍 Troubleshooting

### Backend Not Responding
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Restart backend
docker-compose -f docker-compose.prod.yml restart backend

# Check health
curl http://localhost:9000/docs
```

### Frontend Not Loading
```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs frontend

# Restart frontend
docker-compose -f docker-compose.prod.yml restart frontend

# Check health
curl http://localhost:6000
```

### Database Issues
```bash
# Check MySQL
docker-compose -f docker-compose.prod.yml logs mysql

# Check connection
docker-compose -f docker-compose.prod.yml exec backend \
  python -c "from app.db import engine; engine.connect()"
```

---

## 🌐 Nginx

### Check Status
```bash
sudo systemctl status nginx
```

### Restart Nginx
```bash
sudo systemctl restart nginx
```

### Test Config
```bash
sudo nginx -t
```

### View Logs
```bash
sudo tail -f /var/log/nginx/perspectiveconnect_access.log
sudo tail -f /var/log/nginx/perspectiveconnect_error.log
```

---

## 🔐 SSL/HTTPS

### Renew Certificate
```bash
sudo certbot renew
```

### Check Certificate Expiry
```bash
sudo certbot certificates
```

---

## 📊 Monitoring

### Disk Usage
```bash
df -h
du -sh /opt/perspectiveconnect-versions
```

### Memory Usage
```bash
free -h
docker stats --no-stream
```

### Docker Images
```bash
docker images | grep pc_
```

### Clean Docker
```bash
docker system prune -a
```

---

## 🔄 Update Workflows

### Standard Update
```bash
cd /opt/perspectiveconnect
./deploy-versioned.sh
```

### With Database Backup
```bash
# 1. Backup
docker-compose -f docker-compose.prod.yml exec mysql \
  mysqldump -u root -p perspectiveconnect | gzip > backup_pre_deploy.sql.gz

# 2. Deploy
./deploy-versioned.sh

# 3. Verify
curl https://yourdomain.com
```

### Emergency Rollback
```bash
./rollback.sh 1    # Rollback to previous version
```

---

## 🔑 Environment

### Update Environment
```bash
nano backend/.env
docker-compose -f docker-compose.prod.yml restart
```

### Reload All Env Changes
```bash
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🧪 Health Checks

### Quick Health Check
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:9000/docs
curl -s -o /dev/null -w "%{http_code}" http://localhost:6000
```

### Full Test
```bash
# Backend API
curl http://localhost:9000/docs

# Frontend
curl http://localhost:6000

# Database
docker-compose -f docker-compose.prod.yml exec mysql mysql -u root -p -e "SHOW DATABASES;"
```

---

## 📁 File Locations

| Item | Path |
|------|------|
| Current Deployment | `/opt/perspectiveconnect` |
| Version Backups | `/opt/perspectiveconnect-versions` |
| Backend Code | `/opt/perspectiveconnect/backend` |
| Frontend Code | `/opt/perspectiveconnect/frontend` |
| Environment File | `/opt/perspectiveconnect/backend/.env` |
| Nginx Config | `/etc/nginx/sites-available/perspectiveconnect` |
| SSL Certificates | `/etc/letsencrypt/live/yourdomain.com/` |
| Nginx Logs | `/var/log/nginx/` |
| Audio Storage | `/opt/perspectiveconnect/backend/app/storage` |

---

## 🎯 Quick Recipes

### Deploy and Monitor
```bash
./deploy-versioned.sh && docker-compose -f docker-compose.prod.yml logs -f
```

### Rollback if Issue
```bash
./rollback.sh 1 && docker-compose -f docker-compose.prod.yml logs -f
```

### Full System Restart
```bash
docker-compose -f docker-compose.prod.yml down && \
docker-compose -f docker-compose.prod.yml up -d && \
sleep 10 && \
docker-compose -f docker-compose.prod.yml ps
```

### Update and Backup
```bash
./deploy-versioned.sh && \
docker-compose -f docker-compose.prod.yml exec mysql \
mysqldump -u root -p perspectiveconnect | gzip > backup_after_deploy.sql.gz
```

---

## 📞 Quick Links

- **Full Deployment Guide**: [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Versioning Guide**: [VERSIONING.md](./VERSIONING.md)
- **Quick Start**: [QUICKSTART.md](./QUICKSTART.md)
- **Project README**: [README.md](./README.md)

---

## 🆘 Emergency Contacts

When things go wrong:

1. **Check logs first**: `docker-compose -f docker-compose.prod.yml logs`
2. **Try rollback**: `./rollback.sh`
3. **Restart services**: `docker-compose -f docker-compose.prod.yml restart`
4. **Check versions**: `./list-versions.sh`
5. **Review backups**: `ls -la /opt/perspectiveconnect-versions/`

**Remember**: Always have a backup before major changes!
