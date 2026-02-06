# 🔄 PerspectiveConnect - Versioning & Rollback Guide

This guide explains how to deploy new versions of your application with the ability to rollback to previous versions.

---

## 📋 Overview

The versioning system provides:
- ✅ **Versioned Deployments** - Each deployment is tagged with a timestamp
- ✅ **Docker Image Snapshots** - Previous Docker images are saved
- ✅ **Automatic Rollback** - Failed deployments automatically rollback
- ✅ **Manual Rollback** - Easy rollback to any previous version
- ✅ **Version History** - Track all deployments
- ✅ **Automatic Cleanup** - Keep only recent versions to save space

---

## 🗂️ Directory Structure

```
/opt/perspectiveconnect/              # Current deployment
/opt/perspectiveconnect-versions/     # Version history
  ├── v20260204_143022/               # Version 1
  │   ├── backup/                     # Code backup
  │   ├── backend-image.tar.gz        # Backend Docker image
  │   ├── frontend-image.tar.gz       # Frontend Docker image
  │   ├── commit.txt                  # Git commit hash
  │   └── deployment-info.txt         # Deployment metadata
  ├── v20260204_150615/               # Version 2
  │   └── ...
  └── latest -> v20260204_150615/     # Symlink to latest
```

---

## 🚀 Deploying a New Version

### Basic Deployment

```bash
./deploy-versioned.sh
```

This will:
1. ✅ Backup current deployment and Docker images
2. ✅ Pull latest code from git
3. ✅ Build new Docker images with version tags
4. ✅ Deploy new version
5. ✅ Perform health checks
6. ✅ Auto-rollback if health checks fail
7. ✅ Clean up old versions (keeps last 5)

### What Happens During Deployment

```bash
🚀 PerspectiveConnect Versioned Deployment
Version: v20260204_143022

📦 Step 1: Creating version backup...
Backing up current deployment...
Saving current Docker images...
✅ Backup created

📥 Step 2: Pulling latest code...
Current commit: abc1234

🔧 Step 3: Building new version...
✅ Build complete

🔄 Step 4: Deploying new version...
✅ Services started

⏳ Step 5: Waiting for services to be ready...
✅ Health check passed

🧹 Step 6: Cleaning up old versions...
Kept last 5 versions

🎉 Deployment Successful!
```

---

## ⏪ Rolling Back to a Previous Version

### List Available Versions

```bash
./list-versions.sh
```

Output:
```
📦 PerspectiveConnect Deployment History

Current Version: v20260204_150615

Deployment History:
═════════════════════════════════════════════════════════════════

Version: v20260204_150615
  Commit: abc1234
  Time: Tue Feb 4 15:06:15 UTC 2026
  Status: SUCCESS
  Backup Size: 250M

Version: v20260204_143022
  Commit: def5678
  Time: Tue Feb 4 14:30:22 UTC 2026
  Status: SUCCESS
  Backup Size: 248M

Version: v20260204_120000
  Commit: ghi9012
  Time: Tue Feb 4 12:00:00 UTC 2026
  Status: FAILED
  Backup Size: 245M

Total Versions: 3
Total Disk Usage: 750M
```

### Rollback to Previous Version

```bash
./rollback.sh
```

Interactive menu:
```
⏪ PerspectiveConnect Rollback

Available versions:
[0] v20260204_150615 - abc1234 - Tue Feb 4 15:06:15 UTC 2026
[1] v20260204_143022 - def5678 - Tue Feb 4 14:30:22 UTC 2026
[2] v20260204_120000 - ghi9012 - Tue Feb 4 12:00:00 UTC 2026

Select version to rollback to [0-2]: 1
Rolling back to: v20260204_143022

Are you sure? (yes/no): yes

🔄 Step 1: Stopping current services...
🔄 Step 2: Loading previous Docker images...
🔄 Step 3: Starting services...
⏳ Waiting for services...

✅ Rollback Successful!
Rolled back to: v20260204_143022
```

### Automated Rollback (Non-Interactive)

```bash
./rollback.sh 1  # Rollback to version index 1
```

---

## 🧹 Managing Version Storage

### Automatic Cleanup

By default, `deploy-versioned.sh` keeps the 5 most recent versions.

To change this, edit the script:
```bash
KEEP_VERSIONS=10  # Keep 10 versions instead
```

### Manual Cleanup

Clean up old versions manually:

```bash
# Keep 3 most recent versions
./cleanup-versions.sh 3

# Default: keep 5 versions
./cleanup-versions.sh
```

Output:
```
🧹 PerspectiveConnect Version Cleanup

Total versions: 8
Keeping: 3 most recent

Versions to delete: 5

Will delete:
  - v20260201_120000 (245M)
  - v20260202_120000 (246M)
  - v20260203_120000 (247M)
  - v20260203_150000 (248M)
  - v20260204_100000 (249M)

Continue? (yes/no): yes

Deleting old versions...
  Deleting v20260201_120000...
  Deleting v20260202_120000...
  ...

✅ Cleanup complete
Disk usage: 750M
```

---

## 📊 Monitoring Deployments

### View Deployment History

```bash
./list-versions.sh
```

### Check Current Version

```bash
docker inspect --format='{{.Config.Labels.version}}' pc_backend
```

### View Deployment Logs

```bash
# View specific version info
cat /opt/perspectiveconnect-versions/v20260204_143022/deployment-info.txt
```

---

## 🔍 Troubleshooting

### Deployment Failed

If deployment fails, it will automatically rollback:

```
❌ Health check failed!
Backend: 500, Frontend: 200

Rolling back to previous version...
⏪ PerspectiveConnect Rollback
...
✅ Rollback Successful!
```

### Manual Investigation

```bash
# Check why deployment failed
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend

# Try deploying again after fixing issues
./deploy-versioned.sh
```

### Rollback Failed

If rollback fails:

```bash
# Check Docker images
docker images | grep pc_

# Manually load backup images
cd /opt/perspectiveconnect-versions/v20260204_143022
gunzip -c backend-image.tar.gz | docker load
gunzip -c frontend-image.tar.gz | docker load

# Try starting services
docker-compose -f docker-compose.prod.yml up -d
```

### Version Directory Full

If `/opt/perspectiveconnect-versions` is taking too much space:

```bash
# Check disk usage
df -h /opt

# Clean up aggressively (keep only 2 versions)
./cleanup-versions.sh 2

# Or manually delete specific versions
rm -rf /opt/perspectiveconnect-versions/v20260201_*
```

---

## 🎯 Best Practices

### Before Deployment

1. ✅ **Test in staging** first
2. ✅ **Backup database** separately
3. ✅ **Commit and push** code changes
4. ✅ **Review git diff** to understand changes
5. ✅ **Plan for downtime** if needed

### During Deployment

```bash
# Standard deployment
./deploy-versioned.sh

# Monitor logs in another terminal
docker-compose -f docker-compose.prod.yml logs -f
```

### After Deployment

1. ✅ **Test critical features** (login, practice, sessions)
2. ✅ **Check logs** for errors
3. ✅ **Monitor performance**
4. ✅ **Keep terminal open** for 5-10 minutes
5. ✅ **Have rollback ready** if issues arise

### Regular Maintenance

```bash
# Weekly: Review versions
./list-versions.sh

# Monthly: Clean up old versions
./cleanup-versions.sh 5

# After major releases: Test rollback
./rollback.sh
# Then deploy again: ./deploy-versioned.sh
```

---

## 🔐 Database Versioning

**Important:** Docker images don't include database data!

### Before Major Changes

```bash
# Backup database before deployment
mysqldump -u root -p perspectiveconnect | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Or use the backup script from DEPLOYMENT.md
/usr/local/bin/backup-perspectiveconnect-db.sh
```

### Database Migration Strategy

If your deployment includes database schema changes:

1. **Create migration script** in `backend/migrations/`
2. **Run migration** after deployment:
   ```bash
   docker-compose -f docker-compose.prod.yml exec backend python -m alembic upgrade head
   ```
3. **Test thoroughly** before considering deployment successful

### Rollback with Database Changes

If you need to rollback and there were database changes:

```bash
# 1. Rollback application
./rollback.sh

# 2. Rollback database (if you have migrations)
docker-compose -f docker-compose.prod.yml exec backend python -m alembic downgrade -1

# 3. Or restore from backup
gunzip -c backup_20260204_143022.sql.gz | mysql -u root -p perspectiveconnect
```

---

## 📈 Advanced Usage

### Deploy Specific Git Branch/Tag

```bash
# Edit deploy-versioned.sh temporarily
git fetch --all
git checkout tags/v1.2.0  # or branch name
./deploy-versioned.sh
```

### Zero-Downtime Deployment

For production with multiple servers, use blue-green deployment:

1. Deploy to secondary server
2. Test thoroughly
3. Switch load balancer
4. Deploy to primary server

### Custom Version Tags

```bash
# Edit deploy-versioned.sh to add custom version
VERSION="v1.2.0_$(date +%Y%m%d_%H%M%S)"
```

### Notification on Deployment

Add to `deploy-versioned.sh`:

```bash
# At the end of script
curl -X POST https://your-webhook-url \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Deployed version ${VERSION}\"}"
```

---

## 🛡️ Safety Features

### Automatic Health Checks

After each deployment, the script checks:
- ✅ Backend API is responding (200 OK)
- ✅ Frontend is accessible (200 OK)
- ✅ Services are running

### Automatic Rollback on Failure

If health checks fail, the script automatically:
1. Marks deployment as FAILED
2. Loads previous Docker images
3. Restarts services
4. Verifies rollback worked

### Version Backup Integrity

Each version backup includes:
- Complete codebase
- Docker images (backend & frontend)
- Git commit hash
- Deployment timestamp
- Health check results

---

## 📝 Configuration

### Change Number of Kept Versions

Edit `deploy-versioned.sh`:

```bash
KEEP_VERSIONS=10  # Default is 5
```

### Change Versions Directory

Edit all scripts and change:

```bash
VERSIONS_DIR="/opt/perspectiveconnect-versions"
# to
VERSIONS_DIR="/var/versions/perspectiveconnect"
```

### Disable Auto-Cleanup

Comment out in `deploy-versioned.sh`:

```bash
# cd "${VERSIONS_DIR}"
# ls -dt v* | tail -n +$((KEEP_VERSIONS + 1)) | xargs -r rm -rf
```

---

## 🎓 Example Workflows

### Daily Development Deployment

```bash
# Morning: Deploy latest features
./deploy-versioned.sh

# If issues found
./rollback.sh 1

# After fix
./deploy-versioned.sh
```

### Weekly Production Deployment

```bash
# 1. Backup database
/usr/local/bin/backup-perspectiveconnect-db.sh

# 2. Check current state
./list-versions.sh
docker-compose -f docker-compose.prod.yml ps

# 3. Deploy
./deploy-versioned.sh

# 4. Monitor for 30 minutes
docker-compose -f docker-compose.prod.yml logs -f

# 5. If all good, clean up old versions
./cleanup-versions.sh 3
```

### Emergency Rollback

```bash
# Quick rollback to last known good version
./rollback.sh 1

# Verify
curl https://yourdomain.com
docker-compose -f docker-compose.prod.yml ps

# Investigate issue
docker-compose -f docker-compose.prod.yml logs backend | tail -100
```

---

## 📚 Related Documentation

- [DEPLOYMENT.md](./DEPLOYMENT.md) - Full deployment guide
- [QUICKSTART.md](./QUICKSTART.md) - Quick setup guide
- [README.md](./README.md) - Project overview

---

## 🆘 Support

If you encounter issues with versioning:

1. Check version history: `./list-versions.sh`
2. View deployment logs in `/opt/perspectiveconnect-versions/*/deployment-info.txt`
3. Check Docker images: `docker images | grep pc_`
4. Verify disk space: `df -h /opt`
5. Review script logs from terminal output

**Remember:** Always backup your database separately before major deployments!
