# 🚀 Quick Production Deployment

Fast guide to deploy Interactive Story Generator to production.

## Prerequisites

- Docker and Docker Compose installed
- Gemini API key

## Quick Start (3 Steps)

### 1. Setup Environment

```bash
# Copy environment template
cp env_template.txt .env

# Edit .env and add your API keys
nano .env  # or use your favorite editor
```

### 2. Deploy

**Windows:**
```bash
deploy.bat
```

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

**Or manually:**
```bash
docker-compose up -d --build
```

### 3. Access

Open your browser:
- **Direct**: http://localhost:8501
- **Via Nginx**: http://localhost

## Common Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Update application
git pull
docker-compose up -d --build
```

## Production Checklist

- [ ] `.env` file configured with API keys
- [ ] Docker and Docker Compose installed
- [ ] Services running: `docker-compose ps`
- [ ] Application accessible
- [ ] Logs checked: `docker-compose logs`

## SSL/HTTPS Setup

1. Get SSL certificates (Let's Encrypt):
```bash
sudo certbot certonly --standalone -d yourdomain.com
```

2. Place certificates in `nginx/ssl/`:
   - `fullchain.pem`
   - `privkey.pem`

3. Uncomment HTTPS server block in `nginx.conf`

4. Restart nginx:
```bash
docker-compose restart nginx
```

## Troubleshooting

**Services won't start:**
```bash
docker-compose logs
```

**Port already in use:**
- Change port in `docker-compose.yml`: `"8502:8501"`

**API key errors:**
- Check `.env` file exists and has correct keys
- Verify: `docker-compose exec app env | grep API_KEY`

## Full Documentation

See `PRODUCTION.md` for complete deployment guide.

---

**That's it! Your app is now in production! 🎉**

