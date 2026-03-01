# 🎤 PerspectiveConnect

**AI-Powered Presentation Training Platform**

PerspectiveConnect helps users improve their public speaking and presentation skills through AI-powered coaching, voice analysis, and actionable feedback.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-green.svg)
![Node](https://img.shields.io/badge/node-18+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## ✨ Features

### 🎯 Core Features
- **Audio Recording** - Record presentations directly in the browser
- **AI Transcription** - Powered by OpenAI Whisper for accurate speech-to-text
- **Voice Analysis** - Deep analysis of pitch, pacing, loudness, and clarity
- **Intelligent Coaching** - GPT-4o provides specific, actionable feedback
- **Progress Tracking** - Monitor improvement across multiple sessions
- **Session History** - Review past performances and feedback

### 📊 Analytics
- **Delivery Metrics** - Speech rate, pitch variation, loudness stability
- **Content Analysis** - Filler word detection, sentence structure analysis
- **Performance Scores** - Overall, delivery, and content scores
- **Visual Feedback** - Flags for issues like rushed pacing or monotone delivery

### 🎨 User Experience
- **Modern UI** - Clean, responsive interface with glassmorphism design
- **Theme Selector** - Multiple beautiful background themes
- **Real-time Progress** - Visual feedback during AI processing
- **Secure Authentication** - JWT-based user authentication

---

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **OpenAI** - Whisper (transcription) + GPT-4o (coaching)
- **librosa** - Audio feature extraction
- **Parselmouth** - Voice quality analysis (jitter, shimmer, HNR)
- **MySQL** - Relational database
- **SQLAlchemy** - ORM

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Browser MediaRecorder API** - Audio recording

### Infrastructure
- **Docker** - Containerization
- **Nginx** - Reverse proxy
- **Let's Encrypt** - SSL/TLS certificates

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- MySQL 8.0+
- FFmpeg
- OpenAI API Key

### Development Setup

**1. Clone Repository**
```bash
git clone <your-repo-url>
cd perspectiveconnect
```

**2. Backend Setup**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add your OPENAI_API_KEY

# Start database
docker compose up -d mysql

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 9000
```

**3. Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

**4. Access Application**
- Frontend: http://localhost:6000
- Backend API: http://localhost:9000
   - API Docs: http://localhost:9000/docs

---

## 📦 Production Deployment

### 🆕 First Time Deployment

**Never deployed before?** Start here:  
👉 **[FIRST-DEPLOYMENT.md](./docs/FIRST-DEPLOYMENT.md)** - Complete step-by-step guide (30-45 min)

### Quick Production Setup (5 minutes)

Already have a server ready? See [QUICKSTART.md](./docs/QUICKSTART.md) for rapid deployment.

### Versioned Deployments (Recommended)

Deploy with automatic versioning and rollback capability:

```bash
# First deployment
./deploy-versioned.sh

# Future updates
./deploy-versioned.sh

# Rollback if needed
./scripts/rollback.sh

# View deployment history
./list-versions.sh
```

See [VERSIONING.md](./docs/VERSIONING.md) for complete versioning documentation.

### Simple Deployment

Quick deployment command:

```bash
# Configure environment (first time only)
cp .env.production.example backend/.env
nano backend/.env  # Add your production values

# Deploy (uses versioned deployment)
./deploy.sh
# Note: deploy.sh is a shortcut to deploy-versioned.sh
```

### Full Deployment Guide

See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for comprehensive deployment documentation including:
- Docker deployment
- Manual deployment with systemd
- Nginx configuration
- SSL/HTTPS setup with Let's Encrypt
- Security hardening
- Backup strategies
- Monitoring and logging
- Performance optimization

### Quick Reference

See [DEPLOYMENT-CHEATSHEET.md](./DEPLOYMENT-CHEATSHEET.md) for common commands.

---

## 📖 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:9000/docs
- **OpenAPI Schema**: http://localhost:9000/openapi.json

### Key Endpoints

**Authentication**
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user info

**Training Sessions**
- `POST /training/submit` - Submit audio recording for analysis
- `GET /training/sessions` - List user's sessions
- `GET /training/sessions/{id}` - Get session details
- `GET /training/summary` - Get analytics summary

---

## 🏛️ Project Structure

```
perspectiveconnect/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration
│   │   ├── db.py                # Database setup
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   └── training_session.py
│   │   ├── services/            # Business logic
│   │   │   ├── auth_service.py
│   │   │   ├── transcription_service.py
│   │   │   ├── speech_features_service.py
│   │   │   ├── llm_service.py
│   │   │   └── analytics_service.py
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── security.py          # Auth utilities
│   │   └── deps.py              # Dependencies
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js pages
│   │   │   ├── login/
│   │   │   ├── register/
│   │   │   ├── dashboard/
│   │   │   ├── practice/
│   │   │   └── sessions/
│   │   ├── components/          # React components
│   │   │   ├── Nav.tsx
│   │   │   ├── AudioRecorder.tsx
│   │   │   ├── AuthGuard.tsx
│   │   │   └── ui/
│   │   ├── lib/                 # Utilities
│   │   └── styles/
│   ├── package.json
│   ├── Dockerfile
│   └── tailwind.config.ts
├── docker-compose.yml           # Development compose
├── docker-compose.prod.yml      # Production compose
├── scripts/                     # Deployment scripts
│   ├── deploy-versioned.sh     # Main deployment script
│   ├── rollback.sh             # Rollback to previous version
│   ├── list-versions.sh        # List deployment history
│   ├── check-status.sh         # Health check
│   └── cleanup-versions.sh     # Clean old versions
├── docs/                        # Documentation
│   ├── DEPLOYMENT.md           # Full deployment guide
│   ├── QUICKSTART.md           # Quick start guide
│   ├── FIRST-DEPLOYMENT.md     # Step-by-step first deployment
│   ├── VERSIONING.md           # Versioning and rollback guide
│   └── ...                     # Other documentation
├── config/                      # Configuration examples
│   ├── .env.production.example # Environment template
│   └── nginx.conf.example      # Nginx configuration
├── deploy.sh                    # → Symlink to scripts/deploy-versioned.sh
└── README.md                    # This file
```

---

## 🔧 Configuration

### Backend Environment Variables

```env
# OpenAI
OPENAI_API_KEY=sk-your-api-key
MODEL_NAME=gpt-4o

# JWT
JWT_SECRET=your-secret-key
JWT_ALG=HS256
JWT_EXPIRE_DAYS=7

# Database
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=perspectiveconnect

# Storage
AUDIO_STORAGE_DIR=./app/storage
```

### Frontend Environment Variables

```env
NEXT_PUBLIC_API_BASE=http://localhost:9000
```

---

## 🧪 Testing

### Test Registration & Login
```bash
# Register
curl -X POST http://localhost:9000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"testpass123"}'

# Login
curl -X POST http://localhost:9000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"identifier":"testuser","password":"testpass123"}'
```

### Test Practice Workflow
1. Visit http://localhost:6000
2. Register/login
3. Go to Practice page
4. Record a short speech (20-40 seconds)
5. Submit for feedback
6. View results in Session detail page

---

## 📊 Monitoring

### View Logs

**Docker:**
```bash
docker compose logs -f backend
docker compose logs -f frontend
```

**Systemd:**
```bash
sudo journalctl -u perspectiveconnect-backend -f
sudo journalctl -u perspectiveconnect-frontend -f
```

### Check Status

```bash
# Docker
docker compose ps

# Systemd
sudo systemctl status perspectiveconnect-backend
sudo systemctl status perspectiveconnect-frontend
```

---

## 🔒 Security

- ✅ JWT authentication with secure secret
- ✅ Password hashing with bcrypt
- ✅ Environment variable management
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ CORS configuration
- ✅ HTTPS/SSL support
- ✅ Input validation with Pydantic
- ✅ API key protection

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 🆘 Support & Troubleshooting

### Common Issues

**OpenAI API Key Error:**
- Verify your API key in `backend/.env`
- Check API key has sufficient credits

**FFmpeg Not Found:**
```bash
sudo apt install ffmpeg
```

**Database Connection Error:**
- Check MySQL is running: `docker compose ps`
- Verify database credentials in `.env`

**Port Already in Use:**
```bash
# Check what's using port 9000
sudo netstat -tulpn | grep 9000
```

### Get Help

- Check [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for detailed guides
- Review logs for error messages
- Verify all environment variables are set
- Ensure all dependencies are installed

---

## 🎯 Roadmap

- [ ] Real-time speech analysis during recording
- [ ] Advanced analytics dashboard with charts
- [ ] Team collaboration features
- [ ] Mobile app (React Native)
- [ ] Multi-language support
- [ ] Custom coaching prompts
- [ ] Export session reports (PDF)
- [ ] Integration with video platforms

---

## 🙏 Acknowledgments

- OpenAI for Whisper and GPT-4o
- FastAPI framework
- Next.js and React teams
- librosa and Parselmouth libraries
- All open-source contributors

---

**Built with ❤️ using AI-powered technologies**
