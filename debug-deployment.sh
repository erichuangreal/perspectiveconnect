#!/bin/bash

# Debug deployment issues

echo "🔍 PerspectiveConnect Deployment Debug"
echo "======================================"
echo ""

echo "1. Checking Docker containers..."
docker-compose -f docker-compose.prod.yml ps
echo ""

echo "2. Checking backend logs (last 50 lines)..."
echo "-------------------------------------------"
docker-compose -f docker-compose.prod.yml logs --tail=50 backend
echo ""

echo "3. Checking frontend logs (last 50 lines)..."
echo "-------------------------------------------"
docker-compose -f docker-compose.prod.yml logs --tail=50 frontend
echo ""

echo "4. Checking MySQL logs (last 30 lines)..."
echo "-------------------------------------------"
docker-compose -f docker-compose.prod.yml logs --tail=30 mysql
echo ""

echo "5. Testing endpoints..."
echo "-------------------------------------------"
echo "Backend API:"
curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:8000/docs || echo "Cannot connect"

echo "Frontend:"
curl -s -o /dev/null -w "Status: %{http_code}\n" http://localhost:3000 || echo "Cannot connect"
echo ""

echo "6. Checking network..."
docker network ls | grep perspectiveconnect
echo ""

echo "7. Checking disk space..."
df -h | grep -E 'Filesystem|/dev/'
echo ""

echo "======================================"
echo "Debug complete. Check logs above for errors."
