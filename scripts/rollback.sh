#!/bin/bash
set -e

# PerspectiveConnect Rollback Script

DEPLOY_DIR="/opt/perspectiveconnect"
VERSIONS_DIR="/opt/perspectiveconnect-versions"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Ensure we're in the deployment directory
cd "${DEPLOY_DIR}"

echo -e "${RED}⏪ PerspectiveConnect Rollback${NC}"
echo ""

# Check if versions directory exists
if [ ! -d "${VERSIONS_DIR}" ]; then
    echo -e "${RED}❌ No versions directory found${NC}"
    exit 1
fi

# List available versions
echo -e "${BLUE}Available versions:${NC}"
cd "${VERSIONS_DIR}"
versions=($(ls -dt v* 2>/dev/null | head -n 5))

if [ ${#versions[@]} -eq 0 ]; then
    echo -e "${RED}❌ No previous versions found${NC}"
    exit 1
fi

# Display versions with details
for i in "${!versions[@]}"; do
    version="${versions[$i]}"
    if [ -f "${version}/deployment-info.txt" ]; then
        status=$(grep "Status:" "${version}/deployment-info.txt" | cut -d: -f2 | tr -d ' ')
        commit=$(grep "Commit Hash:" "${version}/deployment-info.txt" | cut -d: -f2 | tr -d ' ')
        time=$(grep "Deployment Time:" "${version}/deployment-info.txt" | cut -d: -f2- | xargs)
        
        if [ "$status" == "SUCCESS" ]; then
            echo -e "${GREEN}[$i]${NC} ${version} - ${commit} - ${time}"
        else
            echo -e "${RED}[$i]${NC} ${version} - ${commit} - ${time} (FAILED)"
        fi
    else
        echo -e "[$i] ${version}"
    fi
done

echo ""

# If argument provided, use it; otherwise ask
if [ -n "$1" ]; then
    CHOICE=$1
else
    read -p "Select version to rollback to [0-$((${#versions[@]}-1))]: " CHOICE
fi

# Validate choice
if ! [[ "$CHOICE" =~ ^[0-9]+$ ]] || [ "$CHOICE" -ge ${#versions[@]} ]; then
    echo -e "${RED}❌ Invalid choice${NC}"
    exit 1
fi

ROLLBACK_VERSION="${versions[$CHOICE]}"
echo ""
echo -e "${YELLOW}Rolling back to: ${ROLLBACK_VERSION}${NC}"
echo ""

# Confirm
if [ -z "$1" ]; then
    read -p "Are you sure? (yes/no): " CONFIRM
    if [ "$CONFIRM" != "yes" ]; then
        echo "Rollback cancelled"
        exit 0
    fi
fi

echo -e "${YELLOW}🔄 Step 1: Stopping current services...${NC}"
cd "${DEPLOY_DIR}"
docker-compose -f docker-compose.prod.yml down

echo -e "${YELLOW}🔄 Step 2: Loading previous Docker images...${NC}"

# Load saved images
if [ -f "${VERSIONS_DIR}/${ROLLBACK_VERSION}/backend-image.tar.gz" ]; then
    echo "Loading backend image..."
    gunzip -c "${VERSIONS_DIR}/${ROLLBACK_VERSION}/backend-image.tar.gz" | docker load
fi

if [ -f "${VERSIONS_DIR}/${ROLLBACK_VERSION}/frontend-image.tar.gz" ]; then
    echo "Loading frontend image..."
    gunzip -c "${VERSIONS_DIR}/${ROLLBACK_VERSION}/frontend-image.tar.gz" | docker load
fi

echo -e "${YELLOW}🔄 Step 3: Starting services...${NC}"
cd "${DEPLOY_DIR}"
docker-compose -f docker-compose.prod.yml up -d

echo -e "${YELLOW}⏳ Waiting for services...${NC}"
sleep 10

# Health check
BACKEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs || echo "000")
FRONTEND_HEALTH=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 || echo "000")

echo ""
if [ "$BACKEND_HEALTH" == "200" ] && [ "$FRONTEND_HEALTH" == "200" ]; then
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo -e "${GREEN}✅ Rollback Successful!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════${NC}"
    echo ""
    echo -e "${BLUE}Rolled back to:${NC} ${ROLLBACK_VERSION}"
    echo -e "${BLUE}Backend:${NC} ${BACKEND_HEALTH}"
    echo -e "${BLUE}Frontend:${NC} ${FRONTEND_HEALTH}"
else
    echo -e "${RED}❌ Rollback health check failed!${NC}"
    echo "Backend: ${BACKEND_HEALTH}, Frontend: ${FRONTEND_HEALTH}"
    echo "Please check logs: docker-compose -f docker-compose.prod.yml logs"
    exit 1
fi

echo ""
echo -e "${BLUE}To view logs:${NC}"
echo "  docker-compose -f docker-compose.prod.yml logs -f"
echo ""
