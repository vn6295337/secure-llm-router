# Troubleshooting Guide

This guide helps diagnose and resolve common issues with the LLM Secure Gateway.

## Table of Contents

1. [Health Check Issues](#health-check-issues)
2. [Authentication Problems](#authentication-problems)
3. [API Request Errors](#api-request-errors)
4. [LLM Provider Issues](#llm-provider-issues)
5. [Performance Problems](#performance-problems)
6. [Deployment Issues](#deployment-issues)
7. [Security Concerns](#security-concerns)

## Health Check Issues

### Service Unreachable

**Symptoms**: 
- `/health` endpoint returns 502, 503, or connection timeout
- Application doesn't start

**Possible Causes**:
- Application not running
- Port binding issues
- Firewall/network restrictions
- Insufficient system resources

**Solutions**:
1. Check if the application process is running:
   ```bash
   ps aux | grep uvicorn
   ```
2. Verify port binding:
   ```bash
   netstat -tlnp | grep :8000
   ```
3. Check application logs for startup errors
4. Ensure firewall allows traffic on the application port

### Health Status Unhealthy

**Symptoms**: 
- `/health` returns status "unhealthy"
- Provider field is null or missing

**Possible Causes**:
- Missing or invalid LLM provider API keys
- Misconfigured environment variables
- Provider service unavailable

**Solutions**:
1. Verify environment variables are set correctly:
   ```bash
   cat .env
   ```
2. Check that at least one LLM provider API key is configured
3. Test API keys with provider's API directly
4. Check provider status pages for service outages

## Authentication Problems

### 401 Unauthorized Errors

**Symptoms**: 
- All API requests except `/health` return 401
- Error message: "Invalid or missing API key"

**Possible Causes**:
- Missing `X-API-Key` header
- Invalid API key value
- `SERVICE_API_KEY` environment variable not set
- API key mismatch between client and server

**Solutions**:
1. Verify the `X-API-Key` header is included in requests:
   ```bash
   curl -H "X-API-Key: your_api_key" http://localhost:8000/query
   ```
2. Check that `SERVICE_API_KEY` is set in environment:
   ```bash
   echo $SERVICE_API_KEY
   ```
3. Ensure API key values match between client and server
4. Regenerate API key if it may have been compromised

### API Key Rejected Despite Being Correct

**Symptoms**: 
- Valid API key is rejected
- Works intermittently

**Possible Causes**:
- Timing attacks prevention causing delays
- Character encoding issues
- Whitespace in API key

**Solutions**:
1. Strip whitespace from API key:
   ```bash
   # Remove any trailing/leading whitespace
   SERVICE_API_KEY=$(echo "$SERVICE_API_KEY" | tr -d ' \t\n\r')
   ```
2. Ensure consistent character encoding (UTF-8)
3. Regenerate API key with alphanumeric characters only

## API Request Errors

### 422 Validation Errors

**Symptoms**: 
- Requests return 422 with validation error messages
- Specific field errors in response

**Possible Causes**:
- Prompt too short or too long
- Invalid `max_tokens` value
- Invalid `temperature` value
- Prompt injection detected

**Solutions**:
1. Check prompt length (1-4000 characters)
2. Verify `max_tokens` is between 1-2048
3. Verify `temperature` is between 0.0-2.0
4. Review prompt for injection patterns like "ignore previous instructions"

### 429 Rate Limit Exceeded

**Symptoms**: 
- Requests return 429 status code
- Error message: "Rate limit exceeded"

**Possible Causes**:
- Too many requests from the same IP within the time window
- Misconfigured rate limit settings
- Shared proxy/IP affecting multiple users

**Solutions**:
1. Reduce request frequency to stay within limits
2. Increase rate limit in configuration:
   ```bash
   RATE_LIMIT=20/minute
   ```
3. Implement exponential backoff in client code
4. Use different IP addresses or API keys for different clients

### 500 Internal Server Errors

**Symptoms**: 
- Requests return 500 with generic error messages
- "All LLM providers failed" error

**Possible Causes**:
- All configured LLM providers are unavailable
- Network connectivity issues
- Provider API key issues
- Application bugs

**Solutions**:
1. Check LLM provider status pages
2. Verify all API keys are valid and have sufficient quotas
3. Test network connectivity to provider endpoints
4. Check application logs for specific error details
5. Try configuring additional LLM providers

## LLM Provider Issues

### Provider Timeout

**Symptoms**: 
- Slow responses or timeouts
- Fallback to secondary providers

**Possible Causes**:
- Provider API latency
- Network connectivity issues
- Provider rate limits exceeded
- Geographic distance from provider

**Solutions**:
1. Check provider status dashboards
2. Verify network connectivity:
   ```bash
   ping generativelanguage.googleapis.com
   ```
3. Review provider rate limits and quotas
4. Consider using providers geographically closer to your deployment

### Provider Returns Empty Response

**Symptoms**: 
- Valid responses with empty content
- Provider used but no text returned

**Possible Causes**:
- Provider API response format changed
- Content filtering blocking response
- Invalid request parameters

**Solutions**:
1. Check provider documentation for response format changes
2. Review content moderation settings
3. Verify request parameters are within acceptable ranges
4. Test with provider's API directly using same parameters

### Provider Quota Exhausted

**Symptoms**: 
- Sudden increase in errors from specific provider
- Provider-specific error messages about quotas

**Possible Causes**:
- Exceeded free tier limits
- Reached paid quota limits
- Billing issues with provider

**Solutions**:
1. Check provider dashboard for quota usage
2. Upgrade to paid tier if using free tier
3. Verify billing information with provider
4. Distribute load across multiple providers

## Performance Problems

### Slow Response Times

**Symptoms**: 
- High latency in API responses
- User experience degradation

**Possible Causes**:
- Slow LLM provider responses
- Network latency
- Insufficient server resources
- Concurrent request overload

**Solutions**:
1. Monitor provider response times individually
2. Optimize network routing
3. Scale server resources (CPU, memory)
4. Implement caching for common requests
5. Use faster LLM providers when possible

### High Memory Usage

**Symptoms**: 
- Application crashes with out-of-memory errors
- System slowdown

**Possible Causes**:
- Memory leaks in application
- Large response payloads
- Too many concurrent requests

**Solutions**:
1. Monitor memory usage over time
2. Implement response size limits
3. Add memory limits to container configuration
4. Scale horizontally with multiple instances

## Deployment Issues

### Docker Container Won't Start

**Symptoms**: 
- Container exits immediately
- Error messages in docker logs

**Possible Causes**:
- Missing environment variables
- Port conflicts
- Incorrect image tag
- Insufficient permissions

**Solutions**:
1. Check container logs:
   ```bash
   docker logs container_name
   ```
2. Verify all required environment variables are set
3. Check for port conflicts:
   ```bash
   docker run -p 8001:8000 ...  # Use different port
   ```
4. Ensure proper permissions for mounted volumes

### Environment Variables Not Loaded

**Symptoms**: 
- Configuration values not applied
- Default values used instead

**Possible Causes**:
- Incorrect .env file format
- Environment file not mounted properly
- Variable names don't match expected names

**Solutions**:
1. Verify .env file format (no spaces around =):
   ```
   SERVICE_API_KEY=your_key_here
   ```
2. Check that environment file is properly mounted in Docker:
   ```bash
   docker run --env-file .env ...
   ```
3. Confirm variable names match documentation

## Security Concerns

### Suspicious Activity Detected

**Symptoms**: 
- Unexpected traffic patterns
- High rate of blocked requests
- Unusual API usage

**Possible Causes**:
- Automated scanning/bot activity
- Compromised API keys
- Misconfigured rate limiting

**Solutions**:
1. Review access logs for suspicious patterns
2. Rotate potentially compromised API keys
3. Implement IP whitelisting if appropriate
4. Add more restrictive rate limiting

### Prompt Injection Attempts

**Symptoms**: 
- High number of requests with injection patterns
- Blocked requests with injection warnings

**Possible Causes**:
- Malicious users attempting to bypass security
- Legitimate users inadvertently triggering filters
- Overly aggressive injection detection

**Solutions**:
1. Review blocked prompts to identify false positives
2. Fine-tune injection detection patterns if needed
3. Implement additional security layers
4. Monitor for patterns in attack attempts

## Getting Additional Help

If you're unable to resolve an issue:

1. Check the [GitHub Issues](https://github.com/vn6295337/LLM-secure-gateway/issues) for similar problems
2. Review application logs for detailed error messages
3. Ensure you're using the latest version of the application
4. Contact the development team with:
   - Detailed description of the problem
   - Steps to reproduce
   - Relevant log excerpts
   - Environment information