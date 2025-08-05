# CarbonCompliance Agent Download Application

A production-ready FastAPI application for downloading CarbonCompliance agents across different operating systems.

## 🌐 **Live Application**

- **Domain**: `https://carboncomplianceagent.carbonteq.build`
- **Purpose**: Standalone agent download page
- **Main Dashboard**: `https://carboncompliance.carbonteq.build`

## 🚀 **Features**

### **Multi-Platform Support**
- **macOS**: Native binary with one-command installation
- **Linux**: Native binary with one-command installation  
- **Windows**: Native binary with PowerShell installation

### **Security & Safety**
- **Read-Only Operations**: Agent only reads system information
- **No Data Collection**: Only sends compliance metrics, no personal data
- **Secure Communication**: HTTPS with certificate validation
- **Lightweight**: Minimal resource usage
- **Transparent**: All activities logged locally
- **No Remote Access**: Cannot be used for remote control

### **User Experience**
- **Single Command**: One-liner installation for each platform
- **Auto-Registration**: Agent automatically registers with dashboard
- **Daily Reports**: Automatic compliance reports at 12 AM Pakistani time
- **Clean Interface**: Professional download page with security information

## 📋 **What the Agent Monitors**

- **Disk Encryption**: FileVault (macOS), LUKS (Linux), BitLocker (Windows)
- **OS Updates**: System updates and security patches
- **Security Policies**: Password policies, firewall settings
- **Compliance Scoring**: Real-time scoring based on industry standards

## 🛠️ **Technology Stack**

- **Backend**: FastAPI (Python)
- **Frontend**: HTML/CSS/JavaScript
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Registry**: Docker Hub

## 🚀 **Quick Start**

### **Local Development**

```bash
# Clone the repository
git clone https://github.com/saadhaniftaj/Endpoint-Compliance-Monitor-using-DevOps-practices-Agent.git
cd Endpoint-Compliance-Monitor-using-DevOps-practices-Agent

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### **Docker Deployment**

```bash
# Build the image
docker build -t carboncompliance-agent-download .

# Run the container
docker run -p 8080:8080 carboncompliance-agent-download
```

### **Production Deployment**

```bash
# Pull from Docker Hub
docker pull saadhaniftaj/endpoint-agent:latest

# Run with domain configuration
docker run -p 8080:8080 \
  -e DOMAIN=carboncomplianceagent.carbonteq.build \
  saadhaniftaj/endpoint-agent:latest
```

## 📦 **Docker Images**

- **Repository**: `saadhaniftaj/endpoint-agent`
- **Tags**: `latest`, `v1.0.0`, `v1.1.0`, etc.
- **Architecture**: Multi-platform support

## 🔄 **CI/CD Pipeline**

### **GitHub Actions Workflow**
- **Trigger**: Git tags starting with `v*`
- **Build**: Automated Docker image build
- **Push**: Automatic push to Docker Hub
- **Registry**: `saadhaniftaj/endpoint-agent`

### **Deployment Process**
1. Create and push a new tag: `git tag v1.2.0 && git push origin v1.2.0`
2. GitHub Actions automatically builds and pushes to Docker Hub
3. Pull and deploy on your VM: `docker pull saadhaniftaj/endpoint-agent:v1.2.0`

## 🌐 **API Endpoints**

### **Download Information**
- `GET /api/download/{os_type}` - Get download commands for specific OS
- **Supported OS**: `macos`, `linux`, `windows`

### **Health Check**
- `GET /health` - Application health status

### **Static Files**
- `GET /` - Main download page
- `GET /static/*` - Static assets (HTML, CSS, images)

## 📊 **Example API Response**

```json
{
  "binary_name": "carboncompliance-agent-macos",
  "download_url": "https://carboncomplianceagent.carbonteq.build/downloads/carboncompliance-agent-macos",
  "single_command": "curl -s https://carboncomplianceagent.carbonteq.build/downloads/carboncompliance-agent-macos -o carboncompliance-agent-macos && chmod +x carboncompliance-agent-macos && ./carboncompliance-agent-macos --api-url=https://carboncompliance.carbonteq.build",
  "instructions": "chmod +x carboncompliance-agent-macos && ./carboncompliance-agent-macos --api-url=https://carboncompliance.carbonteq.build"
}
```

## 🔧 **Configuration**

### **Environment Variables**
- `DOMAIN`: Application domain (default: localhost)
- `PORT`: Application port (default: 8080)

### **Domain Configuration**
- **Download URLs**: `https://carboncomplianceagent.carbonteq.build/downloads/`
- **Agent API**: `https://carboncompliance.carbonteq.build`

## 🛡️ **Security Features**

- **HTTPS Only**: All communications encrypted
- **Non-Root User**: Container runs as non-root user
- **Health Checks**: Regular health monitoring
- **Input Validation**: All inputs validated and sanitized
- **CORS Configuration**: Proper CORS headers
- **Error Handling**: Comprehensive error handling

## 📈 **Monitoring**

- **Health Endpoint**: `/health` for monitoring
- **Logging**: Structured logging with different levels
- **Metrics**: Request/response metrics
- **Error Tracking**: Comprehensive error logging

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 **License**

This project is part of the CarbonCompliance endpoint monitoring system.

## 👨‍💻 **Author**

- **GitHub**: [@saadhaniftaj](https://github.com/saadhaniftaj)
- **Project**: DevOps Final Project

---

**Note**: This application is designed to work with the main CarbonCompliance dashboard at `https://carboncompliance.carbonteq.build`. 