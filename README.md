# CarbonCompliance Agent Download Center

A standalone web application for downloading CarbonCompliance agents across different operating systems.

## 🚀 Features

- **Multi-Platform Support**: Download agents for macOS, Linux, and Windows
- **Zero Configuration**: Simple one-click downloads with clear instructions
- **Modern UI**: Beautiful, responsive interface matching the CarbonCompliance brand
- **Standalone**: Completely independent from the main dashboard application
- **Docker Ready**: Easy deployment with Docker and Docker Compose

## 📋 Prerequisites

- Python 3.11+ or Docker
- FastAPI and Uvicorn (if running locally)

## 🛠️ Local Development

### Option 1: Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Option 2: Docker

```bash
# Build and run with Docker
docker build -t carboncompliance-download .
docker run -p 8080:8080 carboncompliance-download

# Or use Docker Compose
docker-compose up -d
```

## 🌐 Access

Once running, access the application at:
- **Local**: http://localhost:8080
- **Docker**: http://localhost:8080

## 📁 Project Structure

```
download-app/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
├── README.md           # This file
└── static/
    ├── download.html   # Main download page
    ├── styles.css      # CSS styles (if needed)
    └── carbonteq_logo.jpeg  # Logo file
```

## 🔧 Configuration

### Environment Variables

- `DOMAIN`: Your domain for download URLs (default: your-domain.com)

### Customizing Download URLs

Edit the `download_info` dictionary in `main.py` to update:
- Download URLs for each platform
- API endpoints for agent configuration
- Custom instructions

## 🚀 Deployment

### Docker Deployment

```bash
# Build and deploy
docker build -t carboncompliance-download .
docker run -d -p 8080:8080 --name download-app carboncompliance-download
```

### Docker Compose Deployment

```bash
# Deploy with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### Production Deployment

For production deployment:

1. **Update Domain**: Change `your-domain.com` to your actual domain
2. **SSL Certificate**: Add SSL/TLS certificate for HTTPS
3. **Reverse Proxy**: Use Nginx or Apache as reverse proxy
4. **Load Balancer**: Add load balancer for high availability

### Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name download.your-domain.com;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 Security Considerations

- **HTTPS**: Always use HTTPS in production
- **Rate Limiting**: Implement rate limiting for download endpoints
- **Access Control**: Consider adding authentication if needed
- **CORS**: Configure CORS properly for your domain

## 📊 Monitoring

### Health Check

The application includes a health check endpoint:
```bash
curl http://localhost:8080/health
```

### Docker Health Check

Docker includes automatic health checks:
```bash
docker ps  # Check container status
docker logs download-app  # View application logs
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using port 8080
   lsof -i :8080
   # Kill the process or change port in main.py
   ```

2. **Docker Build Fails**
   ```bash
   # Clean Docker cache
   docker system prune -a
   # Rebuild
   docker build --no-cache -t carboncompliance-download .
   ```

3. **Static Files Not Loading**
   - Ensure `static/` directory exists
   - Check file permissions
   - Verify file paths in HTML

### Logs

```bash
# View application logs
docker logs download-app

# View Docker Compose logs
docker-compose logs -f
```

## 🔄 Updates

To update the application:

1. **Pull latest code**
2. **Rebuild Docker image**: `docker build -t carboncompliance-download .`
3. **Restart container**: `docker-compose restart`

## 📞 Support

For issues or questions:
- Check the logs for error messages
- Verify configuration settings
- Ensure all dependencies are installed

## 📄 License

This project is part of the CarbonCompliance ecosystem. 