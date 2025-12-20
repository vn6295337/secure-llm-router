# Installation Guide

This guide provides detailed instructions for installing and setting up the LLM Secure Gateway.

## System Requirements

### Minimum Requirements

- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.8 or higher
- **Memory**: 512 MB RAM
- **Disk Space**: 100 MB available space
- **Network**: Internet connectivity for LLM provider APIs

### Recommended Requirements

- **Operating System**: Ubuntu 20.04+, macOS 12+, or Windows 10+
- **Python**: 3.11+
- **Memory**: 1 GB RAM
- **Disk Space**: 500 MB available space
- **Network**: Stable broadband connection

## Installation Methods

### Method 1: Local Installation (Recommended for Development)

#### 1. Clone the Repository

```bash
git clone https://github.com/vn6295337/LLM-secure-gateway.git
cd LLM-secure-gateway
```

#### 2. Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Verify Installation

```bash
python -c "import fastapi, uvicorn, pydantic; print('Installation successful')"
```

### Method 2: Docker Installation (Recommended for Production)

#### 1. Pull the Docker Image

```bash
# Pull the official image (when available)
docker pull llm-secure-gateway:latest

# Or build from source
git clone https://github.com/vn6295337/LLM-secure-gateway.git
cd LLM-secure-gateway
docker build -t llm-secure-gateway .
```

#### 2. Verify Docker Installation

```bash
docker images | grep llm-secure-gateway
```

## Configuration

### Environment Variables

Create a `.env` file with your configuration:

```bash
cp .env.example .env
```

Edit the `.env` file with your settings:

```bash
# Service Configuration
SERVICE_API_KEY=sk-your-secure-api-key-here

# LLM Provider API Keys (at least one required)
GEMINI_API_KEY=your-gemini-api-key
GROQ_API_KEY=your-groq-api-key
OPENROUTER_API_KEY=your-openrouter-api-key

# Optional Configuration
RATE_LIMIT=10/minute
ALLOWED_ORIGINS=*
ENABLE_PROMPT_INJECTION_CHECK=true
```

### Configuration Options

See [Configuration Guide](configuration.md) for detailed configuration options.

## Starting the Service

### Local Development

```bash
# Activate virtual environment if not already activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start the development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production with Docker

```bash
# Run with environment variables
docker run -d \
  -e SERVICE_API_KEY=your_service_api_key \
  -e GEMINI_API_KEY=your_gemini_api_key \
  -e GROQ_API_KEY=your_groq_api_key \
  -e OPENROUTER_API_KEY=your_openrouter_api_key \
  -p 8000:8000 \
  --name llm-gateway \
  llm-secure-gateway

# Or run with environment file
docker run -d \
  --env-file .env \
  -p 8000:8000 \
  --name llm-gateway \
  llm-secure-gateway
```

## Verification

### Check Health Endpoint

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "provider": "gemini",
  "timestamp": 1700000000.123456
}
```

### Test Query Endpoint

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_service_api_key" \
  -d '{
    "prompt": "Hello, world!",
    "max_tokens": 50
  }'
```

## Platform-Specific Instructions

### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv git

# Follow standard installation steps
```

### CentOS/RHEL

```bash
# Install Python and pip
sudo yum install python3 python3-pip git

# Or for newer versions
sudo dnf install python3 python3-pip git

# Follow standard installation steps
```

### macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python git

# Follow standard installation steps
```

### Windows

1. Download and install Python from [python.org](https://www.python.org/downloads/)
2. Install Git from [git-scm.com](https://git-scm.com/downloads)
3. Use PowerShell or Command Prompt for installation steps

## Troubleshooting Installation

### Common Issues

#### 1. Python Version Issues

**Problem**: "Python 3.8 or higher required"

**Solution**:
```bash
# Check Python version
python --version

# If multiple versions installed, use specific version
python3.11 -m venv venv
```

#### 2. Permission Denied

**Problem**: "Permission denied" when installing packages

**Solution**:
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or run with sudo (not recommended)
sudo pip install -r requirements.txt
```

#### 3. Virtual Environment Issues

**Problem**: "Command not found" for pip or python

**Solution**:
```bash
# Activate virtual environment
source venv/bin/activate

# Or on Windows
venv\Scripts\activate

# Verify activation
which python
which pip
```

#### 4. Dependency Installation Failures

**Problem**: Errors during `pip install -r requirements.txt`

**Solution**:
```bash
# Upgrade pip first
pip install --upgrade pip

# Install dependencies one by one to identify problematic packages
pip install fastapi
pip install uvicorn
# ... continue with other packages

# Or try with --no-cache-dir
pip install --no-cache-dir -r requirements.txt
```

#### 5. Docker Build Failures

**Problem**: Errors during `docker build`

**Solution**:
```bash
# Check Docker daemon
docker info

# Clean up Docker cache
docker system prune -a

# Build with no cache
docker build --no-cache -t llm-secure-gateway .
```

### Verifying Installation

After installation, verify all components work correctly:

```bash
# Check Python packages
python -c "import fastapi; print(fastapi.__version__)"
python -c "import uvicorn; print(uvicorn.__version__)"
python -c "import pydantic; print(pydantic.__version__)"

# Check virtual environment
pip list | grep -E "(fastapi|uvicorn|pydantic|slowapi|requests)"

# Test import of application modules
python -c "from src.main import app; print('App imported successfully')"
```

## Post-Installation Steps

### 1. Generate API Keys

Create strong, random API keys for your service:

```bash
# Generate a secure API key
python -c "import secrets; print('sk-' + secrets.token_urlsafe(32))"
```

### 2. Configure Security Settings

Review and adjust security settings in your `.env` file:

```bash
# Restrict CORS in production
ALLOWED_ORIGINS=https://yourdomain.com

# Adjust rate limits as needed
RATE_LIMIT=20/minute
```

### 3. Test All Providers

Verify all configured LLM providers work correctly:

```bash
# Test with each provider by temporarily setting only one API key
# and checking the /health endpoint response
```

### 4. Set Up Monitoring

Configure logging and monitoring for your deployment:

```bash
# Set up log rotation
# Configure health check monitoring
# Set up alerting for errors
```

## Updating the Installation

### Local Installation

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Restart the service
```

### Docker Installation

```bash
# Pull latest image
docker pull llm-secure-gateway:latest

# Stop and remove current container
docker stop llm-gateway
docker rm llm-gateway

# Run new container
docker run -d \
  --env-file .env \
  -p 8000:8000 \
  --name llm-gateway \
  llm-secure-gateway
```

## Uninstalling

### Local Installation

```bash
# Deactivate virtual environment
deactivate

# Remove the directory
rm -rf LLM-secure-gateway

# Optionally remove Python virtual environment
rm -rf venv
```

### Docker Installation

```bash
# Stop and remove container
docker stop llm-gateway
docker rm llm-gateway

# Remove image
docker rmi llm-secure-gateway

# Clean up unused Docker resources
docker system prune -a
```

## Getting Help

If you encounter issues during installation:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Review the application logs for error messages
3. Search [GitHub Issues](https://github.com/vn6295337/LLM-secure-gateway/issues) for similar problems
4. Open a new issue with detailed information about your environment and the problem