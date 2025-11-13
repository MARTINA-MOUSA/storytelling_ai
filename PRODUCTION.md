# Production Deployment Guide

Complete guide for deploying Interactive Story Generator to production.

## Prerequisites

- Docker and Docker Compose installed
- Domain name (optional, for SSL)
- SSL certificates (optional, for HTTPS)
- Server with at least 2GB RAM (4GB+ recommended)
- Google Gemini API key

## Quick Start with Docker

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd storytelling_ai
```

### 2. Environment Setup

Create `.env` file with production values:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Production settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

### 3. Build and Start

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

### 4. Access Application

- **Application**: http://localhost:8501
- **With Nginx**: http://localhost (port 80)

## Production Deployment Options

### Option 1: Docker Compose (Recommended)

**Start services:**
```bash
docker-compose up -d
```

**Stop services:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f app
docker-compose logs -f nginx
```

**Restart services:**
```bash
docker-compose restart
```

### Option 2: Docker Only (Without Nginx)

```bash
# Build image
docker build -t storytelling-ai .

# Run container
docker run -d \
  --name storytelling-ai \
  -p 8501:8501 \
  -e GEMINI_API_KEY=your_key \
  -e HUGGINGFACE_API_KEY=your_key \
  -v $(pwd)/outputs:/app/outputs \
  -v $(pwd)/.env:/app/.env:ro \
  --restart unless-stopped \
  storytelling-ai
```

### Option 3: Direct Python (Without Docker)

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**
```bash
export GEMINI_API_KEY=your_key
export HUGGINGFACE_API_KEY=your_key
```

3. **Run Streamlit:**
```bash
streamlit run frontend/app.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --server.headless=true
```

## SSL/HTTPS Setup

### Using Let's Encrypt

1. **Install Certbot:**
```bash
sudo apt-get update
sudo apt-get install certbot
```

2. **Get SSL certificates:**
```bash
sudo certbot certonly --standalone -d yourdomain.com
```

3. **Update nginx.conf:**
   - Uncomment HTTPS server block
   - Update `server_name` with your domain
   - Update SSL certificate paths

4. **Mount certificates in docker-compose.yml:**
```yaml
nginx:
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf:ro
    - /etc/letsencrypt:/etc/nginx/ssl:ro
```

5. **Update HTTP server to redirect:**
   - Uncomment redirect line in nginx.conf

6. **Restart services:**
```bash
docker-compose restart nginx
```

## Environment Variables

### Required Variables

- `GEMINI_API_KEY` - Google Gemini API key (required)

### Optional Variables

- `HUGGINGFACE_API_KEY` - Hugging Face API key (for better image generation)
- `STREAMLIT_SERVER_PORT` - Port for Streamlit (default: 8501)
- `STREAMLIT_SERVER_ADDRESS` - Server address (default: 0.0.0.0)
- `STREAMLIT_SERVER_HEADLESS` - Run in headless mode (default: true)
- `STREAMLIT_BROWSER_GATHER_USAGE_STATS` - Disable usage stats (default: false)

## Monitoring and Logging

### View Application Logs

```bash
# Docker Compose
docker-compose logs -f app

# Docker
docker logs -f storytelling-ai

# Nginx logs
docker-compose logs -f nginx
```

### Health Check

The application includes a health check endpoint:
- Health endpoint: `http://localhost:8501/_stcore/health`

### Resource Monitoring

```bash
# Container stats
docker stats storytelling-ai

# System resources
docker stats
```

## Scaling

### Horizontal Scaling

For high traffic, you can run multiple instances:

```yaml
# docker-compose.yml
services:
  app:
    # ... existing config
    deploy:
      replicas: 3
```

Or use a load balancer (nginx, traefik, etc.) in front of multiple instances.

### Vertical Scaling

Increase container resources:

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

## Security Best Practices

1. **Never commit `.env` file** - Contains sensitive API keys
2. **Use strong passwords** - For any authentication
3. **Enable HTTPS** - Use SSL certificates
4. **Rate limiting** - Already configured in nginx.conf
5. **Keep dependencies updated** - Regularly update packages
6. **Use secrets management** - For production, use Docker secrets or external secret managers
7. **Firewall rules** - Only expose necessary ports
8. **Regular backups** - Backup outputs directory

## Backup and Recovery

### Backup Outputs

```bash
# Backup outputs directory
tar -czf outputs-backup-$(date +%Y%m%d).tar.gz outputs/

# Restore
tar -xzf outputs-backup-YYYYMMDD.tar.gz
```

### Backup Configuration

```bash
# Backup .env and config files
tar -czf config-backup-$(date +%Y%m%d).tar.gz .env docker-compose.yml nginx.conf
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs app

# Check container status
docker-compose ps

# Restart container
docker-compose restart app
```

### Port already in use

```bash
# Find process using port
lsof -i :8501  # Linux/Mac
netstat -ano | findstr :8501  # Windows

# Change port in docker-compose.yml
ports:
  - "8502:8501"
```

### API key errors

- Verify `.env` file exists and contains correct keys
- Check environment variables: `docker-compose exec app env | grep API_KEY`
- Ensure `.env` file is mounted correctly

### High memory usage

- Reduce number of workers
- Increase container memory limits
- Optimize image generation settings

## Performance Optimization

1. **Use CDN** - For static assets
2. **Enable caching** - In nginx for static content
3. **Optimize images** - Reduce image sizes
4. **Database** - If adding database, use connection pooling
5. **Caching** - Implement Redis for caching API responses

## Updates and Maintenance

### Update Application

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build
```

### Update Dependencies

```bash
# Update requirements.txt
pip install --upgrade package_name

# Rebuild container
docker-compose build --no-cache
docker-compose up -d
```

## Systemd Service (Alternative)

Create `/etc/systemd/system/storytelling-ai.service`:

```ini
[Unit]
Description=Interactive Story Generator
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/storytelling-ai
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable storytelling-ai
sudo systemctl start storytelling-ai
```

## Production Checklist

- [ ] Environment variables configured
- [ ] SSL certificates installed (if using HTTPS)
- [ ] Firewall rules configured
- [ ] Monitoring set up
- [ ] Backups configured
- [ ] Logs rotation configured
- [ ] Health checks working
- [ ] Rate limiting enabled
- [ ] Security headers configured
- [ ] Documentation updated

## Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- Review this guide
- Open an issue on GitHub

---

**Your application is now production-ready! 🚀**

