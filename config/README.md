# Configuration Files

Example configuration files for PerspectiveConnect production deployment.

## Files

### `.env.production.example`
Template for production environment variables.

**Setup:**
```bash
# Copy to backend/.env and fill in your values
cp config/.env.production.example backend/.env
nano backend/.env
```

**Also create root .env for Docker Compose:**
```bash
# Create root .env with passwords and API URL
cat > .env << EOF
DB_PASSWORD=your-strong-password
NEXT_PUBLIC_API_BASE=http://your-server-ip:8000
EOF
```

### `nginx.conf.example`
Example Nginx configuration for reverse proxy with SSL.

**Setup:**
```bash
# Copy to /etc/nginx/sites-available/perspectiveconnect
sudo cp config/nginx.conf.example /etc/nginx/sites-available/perspectiveconnect

# Edit with your domain name
sudo nano /etc/nginx/sites-available/perspectiveconnect

# Enable site
sudo ln -s /etc/nginx/sites-available/perspectiveconnect /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## See Also

- [Deployment Guide](../docs/DEPLOYMENT.md) - Full deployment instructions
- [First Deployment](../docs/FIRST-DEPLOYMENT.md) - Step-by-step first-time setup
