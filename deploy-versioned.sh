#!/bin/bash
set -e

# PerspectiveConnect Versioned Deployment Script
# This script creates versioned deployments with rollback capability

DEPLOY_DIR="/opt/perspectiveconnect"
VERSIONS_DIR="/opt/perspectiveconnect-versions"
VERSION=$(date +%Y%m%d_%H%M%S)
KEEP_VERSIONS=5  # Number of versions to keep

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 PerspectiveConnect Versioned Deployment${NC}"
echo -e "${BLUE}Version: ${VERSION}${NC}"
echo ""

# Check if running from the correct directory
if [ ! -f "backend/app/main.py" ]; then
    echo -e "${RED}❌ Error: Must run from project root directory${NC}"
    exit 1
fi

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo -e "${RED}❌ Error: backend/.env not found!${NC}"
    echo "Please configure your environment first"
    exit 1
fi

# Create versions directory if it doesn't exist
if [ ! -d "${VERSIONS_DIR}" ]; then
    echo "Creating versions directory..."
    sudo mkdir -p "${VERSIONS_DIR}"
    sudo chown $USER:$USER "${VERSIONS_DIR}"
fi

echo -e "${YELLOW}📦 Step 1: Creating version backup...${NC}"

# Create version directory
VERSION_PATH="${VERSIONS_DIR}/v${VERSION}"
mkdir -p "${VERSION_PATH}"

# Copy current deployment to version backup (skip on first deployment)
if [ -d "${DEPLOY_DIR}" ] && [ "$(docker images -q pc_backend:latest 2>/dev/null)" ]; then
    echo "Backing up current deployment..."
    cp -r "${DEPLOY_DIR}" "${VERSION_PATH}/backup" 2>/dev/null || echo "Skipping code backup"
    
    # Save current Docker images (only if they exist)
    echo "Saving current Docker images..."
    if docker image inspect pc_backend:latest >/dev/null 2>&1; then
        docker save pc_backend:latest | gzip > "${VERSION_PATH}/backend-image.tar.gz"
        echo "  Backend image saved"
    else
        echo "  No backend image to backup (first deployment)"
    fi
    
    if docker image inspect pc_frontend:latest >/dev/null 2>&1; then
        docker save pc_frontend:latest | gzip > "${VERSION_PATH}/frontend-image.tar.gz"
        echo "  Frontend image saved"
    else
        echo "  No frontend image to backup (first deployment)"
    fi
else
    echo "First deployment - no previous version to backup"
fi

echo -e "${GREEN}✅ Backup created at ${VERSION_PATH}${NC}"
echo ""

echo -e "${YELLOW}📥 Step 2: Pulling latest code...${NC}"
git fetch --all
git pull origin $(git branch --show-current)
COMMIT_HASH=$(git rev-parse --short HEAD)
echo "Current commit: ${COMMIT_HASH}"
echo "${COMMIT_HASH}" > "${VERSION_PATH}/commit.txt"
echo ""

echo -e "${YELLOW}🔧 Step 3: Building new version...${NC}"

# Build with version tags
docker-compose -f docker-compose.prod.yml build \
    --build-arg VERSION="${VERSION}" \
    --build-arg COMMIT="${COMMIT_HASH}"

# Tag images with version
docker tag pc_backend:latest "pc_backend:v${VERSION}"
docker tag pc_frontend:latest "pc_frontend:v${VERSION}"

echo -e "${GREEN}✅ Build complete${NC}"
echo ""

echo -e "${YELLOW}🔄 Step 4: Deploying new version...${NC}"

# Stop current services gracefully
docker-compose -f docker-compose.prod.yml down

# Start new services
docker-compose -f docker-compose.prod.yml up -d

echo ""
echo -e "${YELLOW}⏳ Step 5: Waiting for services to be ready...${NC}"

# Wait for containers to be healthy
echo "Checking MySQL..."
for i in {1..30}; do
    if docker-compose -f docker-compose.prod.yml ps mysql | grep -q "healthy"; then
        echo "MySQL is ready"
        break
    fi
    echo "Waiting for MySQL... ($i/30)"
    sleep 2
done

echo "Waiting for backend and frontend to start..."
sleep 15

# Health check with retries
echo "Performing health checks..."
BACKEND_HEALTH="000"
FRONTEND_HEALTH="000"

for i in {1..10}; do
    BACKEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs 2>/dev/null || echo "000")
    FRONTEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null || echo "000")
    
    if [ "$BACKEND_HEALTH" == "200" ] && [ "$FRONTEND_HEALTH" == "200" ]; then
        break
    fi
    
    echo "  Attempt $i/10 - Backend: ${BACKEND_HEALTH}, Frontend: ${FRONTEND_HEALTH}"
    sleep 3
done

if [ "$BACKEND_HEALTH" == "200" ] && [ "$FRONTEND_HEALTH" == "200" ]; then
    echo -e "${GREEN}✅ Health check passed${NC}"
    
    # Save deployment info
    cat > "${VERSION_PATH}/deployment-info.txt" <<EOF
Deployment Version: v${VERSION}
Deployment Time: $(date)
Commit Hash: ${COMMIT_HASH}
Backend Health: ${BACKEND_HEALTH}
Frontend Health: ${FRONTEND_HEALTH}
Status: SUCCESS
EOF
    
    # Create symlink to latest
    ln -sfn "${VERSION_PATH}" "${VERSIONS_DIR}/latest"
    
else
    echo -e "${RED}❌ Health check failed!${NC}"
    echo "Backend: ${BACKEND_HEALTH}, Frontend: ${FRONTEND_HEALTH}"
    echo ""
    
    # Show recent logs to help debug
    echo -e "${YELLOW}Recent backend logs:${NC}"
    docker-compose -f docker-compose.prod.yml logs --tail=20 backend
    echo ""
    echo -e "${YELLOW}Recent frontend logs:${NC}"
    docker-compose -f docker-compose.prod.yml logs --tail=20 frontend
    echo ""
    
    # Save failure info
    cat > "${VERSION_PATH}/deployment-info.txt" <<EOF
Deployment Version: v${VERSION}
Deployment Time: $(date)
Commit Hash: ${COMMIT_HASH}
Backend Health: ${BACKEND_HEALTH}
Frontend Health: ${FRONTEND_HEALTH}
Status: FAILED
EOF
    
    echo -e "${RED}Deployment failed. Services are still running for debugging.${NC}"
    echo -e "${YELLOW}Run './debug-deployment.sh' for detailed diagnostics${NC}"
    echo -e "${YELLOW}Or check logs: docker-compose -f docker-compose.prod.yml logs -f${NC}"
    echo ""
    echo "After fixing issues, run './deploy-versioned.sh' again"
    exit 1
fi

echo ""
echo -e "${YELLOW}🧹 Step 6: Cleaning up old versions...${NC}"

# Keep only the last N versions
cd "${VERSIONS_DIR}"
ls -dt v* | tail -n +$((KEEP_VERSIONS + 1)) | xargs -r rm -rf
echo "Kept last ${KEEP_VERSIONS} versions"

echo ""
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}🎉 Deployment Successful!${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Version:${NC} v${VERSION}"
echo -e "${BLUE}Commit:${NC} ${COMMIT_HASH}"
echo -e "${BLUE}Backend:${NC} http://localhost:8000"
echo -e "${BLUE}Frontend:${NC} http://localhost:3000"
echo ""
echo -e "${BLUE}To view logs:${NC}"
echo "  docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo -e "${BLUE}To rollback:${NC}"
echo "  ./rollback.sh"
echo ""
echo -e "${BLUE}To view deployment history:${NC}"
echo "  ./list-versions.sh"
echo ""
