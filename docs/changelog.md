# Changelog

All notable changes to the LLM Secure Gateway project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation suite
- Installation guide
- Quickstart guide
- Development setup guide
- API reference documentation
- Configuration guide
- Deployment guide
- Troubleshooting guide
- Security overview
- Technology stack documentation
- Design decisions documentation
- Coding standards guide
- Testing guide
- Documentation structure and templates

### Changed
- Organized documentation into categorized structure
- Improved documentation consistency and completeness

### Fixed
- Various documentation typos and formatting issues

## [1.0.0] - 2025-12-16

### Added
- Initial release of LLM Secure Gateway
- Multi-provider LLM routing with automatic failover
- API key authentication
- Rate limiting (10 requests/minute per IP)
- Input validation with Pydantic models
- Prompt injection detection
- CORS configuration
- Docker containerization
- Hugging Face Spaces deployment
- Interactive dashboard
- Comprehensive API documentation
- Health check endpoint
- Query endpoint with LLM cascade logic
- Support for Google Gemini, Groq, and OpenRouter providers
- Environment variable configuration
- Detailed README with usage instructions

### Changed
- Refined cascade logic for better provider failover
- Improved error handling and response formatting
- Enhanced security checks and validation
- Optimized performance for faster response times

### Fixed
- Various bug fixes and stability improvements
- Security vulnerability patches
- Performance optimizations

## [0.2.0] - 2025-12-10

### Added
- Beta version with core functionality
- Basic FastAPI implementation
- Initial LLM provider integration
- Simple authentication mechanism
- Basic rate limiting
- Core API endpoints

## [0.1.0] - 2025-12-05

### Added
- Project initialization
- Basic project structure
- Initial documentation
- Setup scripts
- Dependency management

[Unreleased]: https://github.com/vn6295337/LLM-secure-gateway/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/vn6295337/LLM-secure-gateway/compare/v0.2.0...v1.0.0
[0.2.0]: https://github.com/vn6295337/LLM-secure-gateway/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/vn6295337/LLM-secure-gateway/releases/tag/v0.1.0