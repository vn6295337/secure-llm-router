# Development Setup

This guide explains how to set up your development environment for the LLM Secure Gateway project.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment tool (venv or virtualenv)
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/vn6295337/LLM-secure-gateway.git
cd LLM-secure-gateway
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit the `.env` file and add your API keys:

```bash
# Service API Key (for accessing the gateway)
SERVICE_API_KEY=your_secure_api_key

# LLM Provider API Keys (at least one required)
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key

# Optional configuration
RATE_LIMIT=10/minute
ALLOWED_ORIGINS=*
ENABLE_PROMPT_INJECTION_CHECK=true
```

### 5. Run the Development Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Verify Installation

Visit `http://localhost:8000/health` to verify the service is running.

Visit `http://localhost:8000/docs` to access the interactive API documentation.

## Running Tests

To run tests:

```bash
# TODO: Add test commands when tests are implemented
```

## Development Workflow

1. Create a new branch for your feature or bug fix
2. Make your changes
3. Run the development server to test your changes
4. Commit your changes with clear commit messages
5. Push your branch and create a pull request

## Useful Development Commands

```bash
# Run development server
uvicorn src.main:app --reload

# Run with specific host and port
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Check for syntax errors
python -m py_compile src/

# Format code (if using black)
black src/

# Run linter (if using flake8)
flake8 src/
```

## IDE Setup

### VS Code

Recommended extensions:
- Python
- Pylance
- Black Formatter
- Flake8 Lint

### PyCharm

PyCharm should automatically detect the virtual environment and configure the interpreter.

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure you've activated your virtual environment
2. **Port already in use**: Change the port number in the uvicorn command
3. **Environment variables not loaded**: Check that the .env file exists and is properly formatted

### Getting Help

If you encounter issues, check:
- The project README
- Existing GitHub issues
- The development community