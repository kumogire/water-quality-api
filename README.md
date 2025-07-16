# water-quality-api

A FastAPI-based REST API for querying and analyzing water quality data from the USGS Water Quality Portal, with a focus on California rivers.

## ✨ Features

- 🔍 Query water quality data with flexible filters
- 📊 Generate comprehensive reports (Summary, Detailed, Trend Analysis)
- 🏞️ Focus on California rivers and watersheds
- ⚡ Fast, async API built with FastAPI
- 🐳 Docker support for easy deployment
- 📈 Built-in monitoring and logging
- 🧪 Comprehensive test suite

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/usgs-water-quality-api.git
cd usgs-water-quality-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make dev

# Run the application
uvicorn app.main:app --reload

# Visit http://localhost:8000/docs for API documentation
```

### Docker

```bash
# Build and run with Docker
make docker-build
make docker-run

# Or use docker-compose for development
make docker-dev
```

## 📚 Documentation

- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Development Setup](docs/DEVELOPMENT.md)
- [Usage Examples](docs/EXAMPLES.md)

## 🧪 Testing

```bash
# Run all tests
make test

# Run tests with coverage
pytest tests/ --cov=app --cov-report=html

# Run linting
make lint
```

## 📦 Deployment

Deploy to your preferred cloud platform:

```bash
# Google Cloud Run
make deploy-gcp

# AWS ECS
make deploy-aws

# Or follow the deployment guides in docs/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

See [CONTRIBUTING.md](.github/CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.