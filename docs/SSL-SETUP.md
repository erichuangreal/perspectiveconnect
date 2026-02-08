# SSL Setup for pc.appfounder.ca

Step-by-step guide to set up Nginx and Let's Encrypt SSL for PerspectiveConnect.

---

## Prerequisites

✅ Domain configured: `pc.appfounder.ca` → `159.89.112.149`  
✅ Application running on ports 3000 and 8000  
⚠️ Ports 80 and 443 must be open in firewall

---

## Step 1: Install Nginx and Certbot

```bash
# Update system
sudo apt update

# Install Nginx
sudo apt install -y nginx

# Install Certbot for Let's Encrypt
sudo apt install -y certbot python3-certbot-nginx

# Check Nginx status
sudo systemctl status nginx
```

---

## Step 2: Configure Firewall

```bash
# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Remove temporary testing ports (we'll use Nginx now)
sudo ufw delete allow 3000/tcp
sudo ufw delete allow 8000/tcp

# Check firewall status
sudo ufw status
```
if firewall status is inactive
# Ensure SSH is allowed (IMPORTANT!)
sudo ufw allow 22/tcp

# Enable the firewall
sudo ufw enable

# Check status again
sudo ufw status

---

## Step 3: Update Docker Compose to Bind Localhost

Currently your services are exposed to `0.0.0.0`. We need to change them to `127.0.0.1` so only Nginx can access them.

```bash
cd /opt/perspectiveconnect

# Edit docker-compose.prod.yml
nano docker-compose.prod.yml
```

Change these lines:
```yaml
# FROM:
    ports:
      - "0.0.0.0:8000:8000"

# TO:
    ports:
      - "127.0.0.1:8000:8000"

# AND FROM:
    ports:
      - "0.0.0.0:3000:3000"

# TO:
    ports:
      - "127.0.0.1:3000:3000"
```

Then restart:
```bash
docker-compose -f docker-compose.prod.yml restart
```

---

## Step 4: Create Root .env with Domain

```bash
cd /opt/perspectiveconnect

# Update root .env with HTTPS domain
cat > .env << 'EOF'
DB_PASSWORD=7aYF3UCtxdrldWdI7o3JioL8
NEXT_PUBLIC_API_BASE=https://pc.appfounder.ca/api
EOF

# Verify
cat .env
```

---

## Step 5: Deploy with New Configuration

Pull the latest code with CORS updates:

```bash
cd /opt/perspectiveconnect
git pull origin enhanced1

# Redeploy to rebuild frontend with HTTPS API URL
./deploy.sh
```

---

## Step 6: Configure Nginx

```bash
# Copy the example config
sudo cp /opt/perspectiveconnect/config/nginx.conf.example /etc/nginx/sites-available/perspectiveconnect

# Enable the site
sudo ln -s /etc/nginx/sites-available/perspectiveconnect /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

---

## Step 7: Get SSL Certificate

```bash
# Run Certbot (it will automatically configure Nginx)
sudo certbot --nginx -d pc.appfounder.ca

# Follow the prompts:
# - Enter your email address
# - Agree to terms
# - Choose whether to share email (optional)
# - Certbot will automatically configure HTTPS and set up redirects

# Test auto-renewal
sudo certbot renew --dry-run
```

---

## Step 8: Verify HTTPS

Open your browser to:
- **https://pc.appfounder.ca**

You should see:
- ✅ Green lock icon (secure HTTPS)
- ✅ Application loads correctly
- ✅ Can register/login
- ✅ Microphone access works (this was blocked on HTTP!)

---

## Step 9: Test Full Workflow

1. **Register a new user** at https://pc.appfounder.ca/register
2. **Login** with your credentials
3. **Go to Practice page**
4. **Click "Start Recording"** - microphone permission should be requested
5. **Record some speech** (10-30 seconds)
6. **Submit** and wait for AI feedback
7. **Check Dashboard** to see your session history

---

## Troubleshooting

### Nginx won't start
```bash
# Check for errors
sudo nginx -t
sudo journalctl -u nginx -n 50
```

### Can't connect to backend/frontend
```bash
# Check services are running on localhost
curl http://localhost:8000/
curl http://localhost:3000/

# Check Nginx proxy
sudo tail -f /var/log/nginx/perspectiveconnect_error.log
```

### SSL certificate issues
```bash
# Check certificate
sudo certbot certificates

# Renew manually
sudo certbot renew --force-renewal
```

### Microphone still not working
- Make sure you're accessing via HTTPS (not HTTP)
- Check browser console for errors
- Try in incognito/private mode
- Check browser permissions: Settings → Site Settings → Microphone

---

## Automatic Certificate Renewal

Let's Encrypt certificates expire after 90 days. Certbot sets up automatic renewal:

```bash
# Check renewal timer
sudo systemctl status certbot.timer

# Test renewal
sudo certbot renew --dry-run
```

Certbot will automatically renew certificates before they expire.

---

## Security Best Practices

After SSL is working:

### 1. Disable API Documentation in Production
```bash
# Edit backend/app/main.py and remove /docs endpoint
# Or restrict it to specific IPs
```

### 2. Update Firewall
```bash
# Ensure only necessary ports are open
sudo ufw status

# Should show:
# 22/tcp   - SSH
# 80/tcp   - HTTP (redirects to HTTPS)
# 443/tcp  - HTTPS
```

### 3. Enable HSTS (HTTP Strict Transport Security)
This is already configured in the Nginx config!

---

## Maintenance

### View Access Logs
```bash
sudo tail -f /var/log/nginx/perspectiveconnect_access.log
```

### View Error Logs
```bash
sudo tail -f /var/log/nginx/perspectiveconnect_error.log
```

### Reload Nginx After Config Changes
```bash
sudo nginx -t && sudo systemctl reload nginx
```

---

## Complete! 🎉

Your application is now:
- ✅ Running on HTTPS with valid SSL
- ✅ Secure (green lock in browser)
- ✅ Microphone access enabled
- ✅ Protected by firewall
- ✅ Auto-renewing certificates

Access your app at: **https://pc.appfounder.ca**
