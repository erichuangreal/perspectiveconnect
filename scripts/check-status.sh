#!/bin/bash

# Quick status check script

cd /opt/perspectiveconnect

echo "🔍 Quick Status Check"
echo "===================="
echo ""

echo "Services:"
docker-compose -f docker-compose.prod.yml ps
echo ""

echo "Backend health:"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:9000/docs || echo "Cannot connect to backend"
echo ""

echo "Frontend health:"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:4000 || echo "Cannot connect to frontend"
echo ""

echo "To view logs:"
echo "  Backend:  docker-compose -f docker-compose.prod.yml logs backend"
echo "  Frontend: docker-compose -f docker-compose.prod.yml logs frontend"
echo ""
