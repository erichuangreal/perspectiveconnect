# 📚 PerspectiveConnect - Documentation Index

Quick reference to all deployment and project documentation.

---

## 🎯 Getting Started

### For First-Time Deployment

**👉 [FIRST-DEPLOYMENT.md](./FIRST-DEPLOYMENT.md)** ⭐ START HERE  
Complete step-by-step guide for deploying from scratch (30-45 min)

**Topics covered:**
- Server setup
- Installing all dependencies
- Cloning repository
- Configuring environment
- Running first deployment
- Setting up Nginx + SSL
- Configuring firewall
- Testing & verification

---

## 🚀 Deployment Guides

### Quick Reference

**[QUICKSTART.md](./QUICKSTART.md)**  
5-minute deployment for experienced users with servers already set up

**[DEPLOYMENT-CHEATSHEET.md](./DEPLOYMENT-CHEATSHEET.md)**  
Quick command reference and common operations

### Complete Guides

**[DEPLOYMENT.md](./DEPLOYMENT.md)**  
Comprehensive deployment documentation

**Topics:**
- Docker deployment (recommended)
- Manual deployment with systemd
- Nginx configuration
- SSL/HTTPS setup
- Security hardening
- Backup strategies
- Monitoring & logging
- Performance optimization
- Troubleshooting

**[VERSIONING.md](./VERSIONING.md)**  
Version management and rollback system

**Topics:**
- How versioning works
- Deploying new versions
- Rolling back to previous versions
- Managing version history
- Database versioning
- Best practices
- Troubleshooting rollbacks

---

## 📖 Project Documentation

### Main Documentation

**[README.md](./README.md)**  
Project overview and general information

**Topics:**
- Feature overview
- Tech stack
- Development setup
- API documentation
- Project structure
- Contributing guidelines

### Configuration Files

**[backend/.env.example](./backend/.env.example)**  
Backend environment variables template

**[.env.production.example](./.env.production.example)**  
Production environment variables template

**[nginx.conf.example](./nginx.conf.example)**  
Nginx reverse proxy configuration template

---

## 🛠️ Scripts

### Deployment Scripts

| Script | Purpose |
|--------|---------|
| `deploy-versioned.sh` | Deploy new version with backup (main script) |
| `deploy.sh` | Symlink to deploy-versioned.sh |
| `rollback.sh` | Rollback to previous version |
| `list-versions.sh` | Show deployment history |
| `cleanup-versions.sh` | Clean up old version backups |

### Usage

```bash
# Regular deployment
./deploy-versioned.sh

# View versions
./list-versions.sh

# Rollback
./rollback.sh

# Cleanup
./cleanup-versions.sh 3  # Keep 3 versions
```

---

## 🎓 By Use Case

### "I'm deploying for the first time"
1. **[FIRST-DEPLOYMENT.md](./FIRST-DEPLOYMENT.md)** ⭐
2. Then bookmark **[DEPLOYMENT-CHEATSHEET.md](./DEPLOYMENT-CHEATSHEET.md)**

### "I need to update my deployment"
1. **[VERSIONING.md](./VERSIONING.md)** - Read deployment workflow
2. Run `./deploy-versioned.sh`
3. Use **[DEPLOYMENT-CHEATSHEET.md](./DEPLOYMENT-CHEATSHEET.md)** for commands

### "Something went wrong, I need to rollback"
1. **[VERSIONING.md](./VERSIONING.md)** - Read rollback section
2. Run `./rollback.sh`

### "I'm setting up advanced features"
1. **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Complete reference
   - Security hardening
   - Performance tuning
   - Monitoring setup

### "I'm developing locally"
1. **[README.md](./README.md)** - Development setup section
2. Set up backend and frontend
3. Test features locally

### "I need quick commands"
1. **[DEPLOYMENT-CHEATSHEET.md](./DEPLOYMENT-CHEATSHEET.md)** ⭐

---

## 📊 Visual Guides

**[.github/deployment-flow.md](./.github/deployment-flow.md)**  
Visual diagrams of deployment processes

**Includes:**
- First-time deployment flow
- Regular update process
- Rollback process
- Architecture overview
- Security layers
- Backup strategy

---

## 🔍 By Topic

### Security
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Security Hardening section
- [nginx.conf.example](./nginx.conf.example) - Security headers
- [.github/deployment-flow.md](./.github/deployment-flow.md) - Security layers

### Backups
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Backup Strategy section
- [VERSIONING.md](./VERSIONING.md) - Version backups
- [FIRST-DEPLOYMENT.md](./FIRST-DEPLOYMENT.md) - Setup backups

### Monitoring
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Monitoring and Logs section
- [DEPLOYMENT-CHEATSHEET.md](./DEPLOYMENT-CHEATSHEET.md) - Quick monitoring commands

### Troubleshooting
- [FIRST-DEPLOYMENT.md](./FIRST-DEPLOYMENT.md) - Troubleshooting section
- [VERSIONING.md](./VERSIONING.md) - Rollback troubleshooting
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Troubleshooting section
- [DEPLOYMENT-CHEATSHEET.md](./DEPLOYMENT-CHEATSHEET.md) - Quick fixes

### Performance
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Performance Optimization section

---

## 📂 File Organization

```
perspectiveconnect/
├── 📖 DOCUMENTATION
│   ├── README.md                      # Project overview
│   ├── FIRST-DEPLOYMENT.md            # ⭐ Start here for first deployment
│   ├── QUICKSTART.md                  # 5-minute deployment
│   ├── DEPLOYMENT.md                  # Complete deployment guide
│   ├── VERSIONING.md                  # Version management
│   ├── DEPLOYMENT-CHEATSHEET.md       # Quick command reference
│   └── DOCUMENTATION-INDEX.md         # This file
│
├── 🔧 CONFIGURATION
│   ├── docker-compose.yml             # Development setup
│   ├── docker-compose.prod.yml        # Production setup
│   ├── nginx.conf.example             # Nginx configuration template
│   ├── backend/.env.example           # Backend environment template
│   └── .env.production.example        # Production environment template
│
├── 🚀 DEPLOYMENT SCRIPTS
│   ├── deploy-versioned.sh            # ⭐ Main deployment script
│   ├── deploy.sh                      # → Symlink to deploy-versioned.sh
│   ├── rollback.sh                    # Rollback to previous version
│   ├── list-versions.sh               # Show deployment history
│   └── cleanup-versions.sh            # Clean old versions
│
├── 💻 APPLICATION CODE
│   ├── backend/                       # FastAPI backend
│   └── frontend/                      # Next.js frontend
│
└── 🎨 VISUAL GUIDES
    └── .github/
        └── deployment-flow.md         # Deployment diagrams
```

---

## 🆘 Quick Help

### "Where do I start?"
→ **[FIRST-DEPLOYMENT.md](./FIRST-DEPLOYMENT.md)**

### "How do I deploy updates?"
→ Run `./deploy-versioned.sh` or see **[VERSIONING.md](./VERSIONING.md)**

### "I need a specific command"
→ **[DEPLOYMENT-CHEATSHEET.md](./DEPLOYMENT-CHEATSHEET.md)**

### "Something's broken"
→ Troubleshooting sections in any guide, or run `./rollback.sh`

### "I want to understand the architecture"
→ **[.github/deployment-flow.md](./.github/deployment-flow.md)**

---

## 💡 Tips

1. **Bookmark DEPLOYMENT-CHEATSHEET.md** for daily operations
2. **Read VERSIONING.md** before your first update
3. **Keep FIRST-DEPLOYMENT.md** handy for setting up new servers
4. **Use `./list-versions.sh`** to track your deployments
5. **Always have `./rollback.sh` ready** for emergencies

---

## 📞 Documentation Status

| Document | Status | Last Updated |
|----------|--------|--------------|
| README.md | ✅ Complete | 2026-02-04 |
| FIRST-DEPLOYMENT.md | ✅ Complete | 2026-02-04 |
| QUICKSTART.md | ✅ Complete | 2026-02-04 |
| DEPLOYMENT.md | ✅ Complete | 2026-02-04 |
| VERSIONING.md | ✅ Complete | 2026-02-04 |
| DEPLOYMENT-CHEATSHEET.md | ✅ Complete | 2026-02-04 |
| deployment-flow.md | ✅ Complete | 2026-02-04 |

---

**Happy Deploying! 🚀**
