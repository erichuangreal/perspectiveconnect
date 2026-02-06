#!/bin/bash

# PerspectiveConnect Version History

VERSIONS_DIR="/opt/perspectiveconnect-versions"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}📦 PerspectiveConnect Deployment History${NC}"
echo ""

if [ ! -d "${VERSIONS_DIR}" ]; then
    echo -e "${RED}No deployment history found${NC}"
    exit 0
fi

cd "${VERSIONS_DIR}"

# Check for current version
CURRENT_VERSION=$(docker inspect --format='{{.Config.Labels.version}}' pc_backend 2>/dev/null || echo "unknown")
echo -e "${GREEN}Current Version:${NC} ${CURRENT_VERSION}"
echo ""

# List all versions
echo -e "${BLUE}Deployment History:${NC}"
echo "═════════════════════════════════════════════════════════════════"

versions=($(ls -dt v* 2>/dev/null))

if [ ${#versions[@]} -eq 0 ]; then
    echo "No previous versions found"
    exit 0
fi

for version in "${versions[@]}"; do
    if [ -f "${version}/deployment-info.txt" ]; then
        echo -e "\n${YELLOW}Version:${NC} ${version}"
        
        status=$(grep "Status:" "${version}/deployment-info.txt" | cut -d: -f2 | tr -d ' ')
        commit=$(grep "Commit Hash:" "${version}/deployment-info.txt" | cut -d: -f2 | tr -d ' ')
        time=$(grep "Deployment Time:" "${version}/deployment-info.txt" | cut -d: -f2- | xargs)
        
        echo "  Commit: ${commit}"
        echo "  Time: ${time}"
        
        if [ "$status" == "SUCCESS" ]; then
            echo -e "  Status: ${GREEN}${status}${NC}"
        else
            echo -e "  Status: ${RED}${status}${NC}"
        fi
        
        # Show backup size if exists
        if [ -d "${version}/backup" ]; then
            SIZE=$(du -sh "${version}/backup" | cut -f1)
            echo "  Backup Size: ${SIZE}"
        fi
        
    else
        echo -e "\n${YELLOW}Version:${NC} ${version}"
        echo "  (No deployment info available)"
    fi
done

echo ""
echo "═════════════════════════════════════════════════════════════════"
echo ""
echo -e "${BLUE}Total Versions:${NC} ${#versions[@]}"

# Show disk usage
TOTAL_SIZE=$(du -sh "${VERSIONS_DIR}" | cut -f1)
echo -e "${BLUE}Total Disk Usage:${NC} ${TOTAL_SIZE}"

echo ""
echo -e "${BLUE}Commands:${NC}"
echo "  ./rollback.sh          - Rollback to a previous version"
echo "  ./deploy-versioned.sh  - Deploy new version"
echo ""
