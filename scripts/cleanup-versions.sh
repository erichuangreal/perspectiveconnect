#!/bin/bash

# PerspectiveConnect Version Cleanup Script

VERSIONS_DIR="/opt/perspectiveconnect-versions"
KEEP_VERSIONS=${1:-5}  # Default: keep 5 versions

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🧹 PerspectiveConnect Version Cleanup${NC}"
echo ""

if [ ! -d "${VERSIONS_DIR}" ]; then
    echo -e "${YELLOW}No versions directory found${NC}"
    exit 0
fi

cd "${VERSIONS_DIR}"

versions=($(ls -dt v* 2>/dev/null))
total=${#versions[@]}

if [ $total -eq 0 ]; then
    echo "No versions found"
    exit 0
fi

echo "Total versions: ${total}"
echo "Keeping: ${KEEP_VERSIONS} most recent"
echo ""

if [ $total -le $KEEP_VERSIONS ]; then
    echo -e "${GREEN}No cleanup needed${NC}"
    exit 0
fi

to_delete=$((total - KEEP_VERSIONS))
echo -e "${YELLOW}Versions to delete: ${to_delete}${NC}"
echo ""

# Show what will be deleted
echo "Will delete:"
for version in "${versions[@]:$KEEP_VERSIONS}"; do
    if [ -d "${version}" ]; then
        SIZE=$(du -sh "${version}" | cut -f1)
        echo "  - ${version} (${SIZE})"
    fi
done

echo ""
read -p "Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Cleanup cancelled"
    exit 0
fi

echo ""
echo "Deleting old versions..."

for version in "${versions[@]:$KEEP_VERSIONS}"; do
    if [ -d "${version}" ]; then
        echo "  Deleting ${version}..."
        rm -rf "${version}"
    fi
done

echo ""
echo -e "${GREEN}✅ Cleanup complete${NC}"

# Show remaining disk usage
TOTAL_SIZE=$(du -sh "${VERSIONS_DIR}" | cut -f1)
echo "Disk usage: ${TOTAL_SIZE}"
echo ""
