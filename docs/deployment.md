# Deployment Guide

> **Primary Responsibility:** Deployment procedures for all environments (local, Docker, cloud)

This guide explains how to deploy the Enterprise AI Gateway in different environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Deployment](#local-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Production Considerations](#production-considerations)

## Prerequisites

- Docker (for Docker deployment)
- Python 3.8+ (for local deployment)
- Git
- API keys for at least one LLM provider

## Local Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/vn6295337/Enterprise-AI-Gateway.git
cd Enterprise-AI-Gateway
```

### 2. Set Up Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run the Application

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000`.

## Docker Deployment

### 1. Build the Docker Image

```bash
docker build -t llm-secure-gateway .
```

### 2. Run with Environment Variables

```bash
docker run -d \
  -e SERVICE_API_KEY=your_service_api_key \
  -e GEMINI_API_KEY=your_gemini_api_key \
  -e GROQ_API_KEY=your_groq_api_key \
  -e OPENROUTER_API_KEY=your_openrouter_api_key \
  -p 8000:8000 \
  --name llm-gateway \
  llm-secure-gateway
```

### 3. Run with Environment File

Create a `.env` file with your configuration, then:

```bash
docker run -d \
  --env-file .env \
  -p 8000:8000 \
  --name llm-gateway \
  llm-secure-gateway
```

## Cloud Deployment

### Hugging Face Spaces

1. Create a new Space at [https://huggingface.co/new-space](https://huggingface.co/new-space)
2. Choose "Docker" as the SDK
3. Select a Docker image (e.g., `python:3.11-slim`)
4. Add your repository URL
5. In Space settings, add the following secrets:
   - `SERVICE_API_KEY`
   - `GEMINI_API_KEY` (optional)
   - `GROQ_API_KEY` (optional)
   - `OPENROUTER_API_KEY` (optional)

### AWS Deployment

#### Using EC2

1. Launch an EC2 instance with Ubuntu
2. SSH into the instance
3. Install Docker:

```bash
sudo apt update
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
```

4. Deploy the container:

```bash
sudo docker run -d \
  -e SERVICE_API_KEY=your_service_api_key \
  -e GEMINI_API_KEY=your_gemini_api_key \
  -e GROQ_API_KEY=your_groq_api_key \
  -e OPENROUTER_API_KEY=your_openrouter_api_key \
  -p 80:8000 \
  --name llm-gateway \
  llm-secure-gateway
```

#### Using ECS

1. Create an ECS cluster
2. Create a task definition with the container image
3. Configure environment variables in the task definition
4. Create a service to run the task

### Google Cloud Platform

#### Using Compute Engine

1. Create a Compute Engine instance
2. SSH into the instance
3. Install Docker and deploy as above

#### Using Cloud Run

1. Build and push the Docker image to Container Registry
2. Deploy to Cloud Run with environment variables
3. Configure authentication and networking

### Azure

#### Using Virtual Machines

1. Create a VM
2. SSH into the instance
3. Install Docker and deploy as above

#### Using Azure Container Instances

1. Create a container group
2. Specify the image and environment variables
3. Configure networking and authentication

## Production Considerations

### Security

1. **Use HTTPS**: Always deploy with SSL/TLS encryption
2. **Restrict CORS**: Set specific allowed origins instead of `*`
3. **Rotate API Keys**: Regularly rotate service and provider API keys
4. **Monitor Logs**: Set up logging and monitoring
5. **Rate Limiting**: Adjust rate limits based on expected usage

### Performance

1. **Load Balancing**: Use a load balancer for high availability
2. **Auto-scaling**: Configure auto-scaling based on demand
3. **Caching**: Implement caching for frequently requested responses
4. **Database**: Use a production database for storing logs/metrics

### Monitoring

1. **Health Checks**: Implement health checks for load balancers
2. **Metrics**: Collect and monitor performance metrics
3. **Alerts**: Set up alerts for errors and performance issues
4. **Logging**: Centralize logs for debugging and auditing

### Backup and Recovery

1. **Configuration Backup**: Backup environment configurations
2. **Disaster Recovery**: Plan for disaster recovery scenarios
3. **Rollback Strategy**: Have a rollback strategy for deployments

## Environment Configuration

See [Configuration Guide](configuration.md) for complete environment variable reference.

## Troubleshooting

See [Troubleshooting Guide](troubleshooting.md) for detailed help.

**Quick debugging:**
```bash
docker logs llm-gateway     # View logs
docker ps                   # Check running containers
docker exec -it llm-gateway /bin/bash  # Access shell
```

## Maintenance

### Updates

To update the application:

1. Pull the latest code or Docker image
2. Update environment variables if needed
3. Restart the service

### Monitoring

Regular monitoring tasks:

1. Check application logs
2. Monitor API usage and costs
3. Verify LLM provider availability
4. Review security logs

## Scaling

### Vertical Scaling

Increase resources allocated to the container/host:
- More CPU
- More memory
- Better network bandwidth

### Horizontal Scaling

Deploy multiple instances behind a load balancer:
- Use sticky sessions if needed
- Share configuration across instances
- Monitor individual instance health