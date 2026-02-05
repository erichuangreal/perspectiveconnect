#!/bin/bash

# Quick fix script for first deployment issues

cd /opt/perspectiveconnect

echo "🔧 Checking deployment issues..."
echo ""

echo "1. Backend logs (last 30 lines):"
echo "================================"
docker-compose -f docker-compose.prod.yml logs --tail=30 backend
echo ""

echo "2. Frontend logs (last 30 lines):"
echo "================================="
docker-compose -f docker-compose.prod.yml logs --tail=30 frontend
echo ""

echo "3. Container status:"
echo "===================="
docker-compose -f docker-compose.prod.yml ps
echo ""

echo "Press Enter to continue with restart, or Ctrl+C to cancel"
read

echo "4. Restarting services..."
docker-compose -f docker-compose.prod.yml restart
echo ""

echo "5. Waiting 30 seconds for services to start..."
sleep 30
echo ""

echo "6. Health check:"
echo "================"
echo "Backend:"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:8000/docs || echo "Still not responding"

echo "Frontend:"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:3000 || echo "Still not responding"
echo ""

echo "If still failing, check logs above for specific errors."
