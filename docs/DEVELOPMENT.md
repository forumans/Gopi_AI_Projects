# Development Guide

## 🛠 Development Setup

### Prerequisites
- Python 3.8 or higher
- Git for version control
- Code editor (VS Code recommended)

### Environment Setup

#### 1. Clone Repository
```bash
git clone <repository-url>
cd phidata_multi_agent_app
```

#### 2. Create Virtual Environment and activate it
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Environment Variables
```bash
# Copy environment template
cp .env.example .env

# Edit with your settings
notepad .env
```

## 🏗️ Project Structure

```
phidata_multi_agent_app/
├── app.py                  # Main entry point
├── src/
│   └── app.py             # Complete application
├── unit_test/              # Unit tests
│   ├── test_financial_analysis.py
│   └── run_tests.py
├── e2e_tests/             # End-to-end tests
│   ├── test_ui_end_to_end.py
│   └── README.md
├── docs/                   # Documentation
│   ├── README.md          # Main documentation
│   ├── TESTING.md         # Testing guide
│   └── DEVELOPMENT.md     # This file
├── requirements.txt        # Dependencies
├── Dockerfile            # Container config
├── docker-compose.yml   # Multi-container config
├── .gitignore           # Git ignore rules
└── .env                 # Environment variables
```
## Create a Mermaid diagram for the project structure

```mermaid
graph TD
    A[phidata_multi_agent_app] --> B[app.py]
    A --> C[src]
    C --> D[app.py]
    A --> E[unit_test]
    E --> F[test_financial_analysis.py]
    E --> G[run_tests.py]
    A --> H[e2e_tests]
    H --> I[test_ui_end_to_end.py]
    H --> J[README.md]
    A --> K[docs]
    K --> L[README.md]
    K --> M[TESTING.md]
    K --> N[DEVELOPMENT.md]
    A --> O[requirements.txt]
    A --> P[Dockerfile]
    A --> Q[docker-compose.yml]
    A --> R[.gitignore]
    A --> S[.env]

## Project Structure Diagram
![alt text](<phidata Multi-Agent App-2026-03-01-035745.png>)


## 🧪 Development Workflow

### 1. Local Development
```bash
# Start the application
python app.py

# Access at http://localhost:7860
```

### 2. Testing Your Changes

#### Unit Tests
```bash
# Quick validation
python unit_test/run_tests.py

# Comprehensive tests
python unit_test/test_financial_analysis.py
```

#### End-to-End Tests
```bash
# Install Playwright (if not already installed)
pip install playwright
playwright install chromium

# Run E2E tests
cd e2e_tests
python test_ui_end_to_end.py
```

### 3. Code Quality

#### Running Tests Before Commit
```bash
# Ensure all tests pass
python unit_test/run_tests.py
python e2e_tests/test_ui_end_to_end.py

# Only commit if tests pass
git add .
git commit -m "feat: add new feature with tests"
```

#### Code Style
- **Python**: Follow PEP 8 guidelines
- **Functions**: Use descriptive names and docstrings
- **Error Handling**: Provide helpful error messages
- **Comments**: Explain complex logic

### 4. Adding New Features

#### Step 1: Understand Requirements
- Identify the user need
- Review existing code structure
- Plan the implementation approach

#### Step 2: Implementation
```python
# Modify src/app.py
# Add new function or modify existing
# Follow existing patterns and style
```

#### Step 3: Testing
```python
# Add unit tests
python unit_test/test_financial_analysis.py

# Add E2E tests
python e2e_tests/test_ui_end_to_end.py

# Verify all tests pass
```

#### Step 4: Documentation
```markdown
# Update docs/README.md
# Update relevant sections
# Add examples for new features
```

## 🔧 Debugging

### Common Development Issues

#### Import Errors
```python
# Check Python path
import sys
print(sys.path)

# Add src to path if needed
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
```

#### Port Conflicts
```bash
# Check what's using port 7860
netstat -ano | findstr :7860

# Kill process if needed
taskkill /PID <process_id> /F
```

#### API Issues
```python
# Test API connectivity
import requests
response = requests.get('https://api.example.com')
print(response.status_code)
```

### Debug Mode
```bash
# Enable debug mode
export DEBUG=true
python app.py
```

## 🧪 Testing in Development

### Test-Driven Development
1. **Write Test First**: Create test before implementation
2. **Run Tests**: Validate current functionality
3. **Implement Feature**: Write code to pass tests
4. **Refactor**: Improve while maintaining test coverage
5. **Document**: Update documentation

### Local Testing Commands
```bash
# Run specific test category
python -m pytest unit_test/test_financial_analysis.py::TestFinancialAnalysis::test_web_search_success

# Run with coverage
python -m pytest --cov=src unit_test/

# Generate coverage report
python -m pytest --cov=src --cov-report=html unit_test/
```

## 🚀 Deployment Preparation

### Pre-Deployment Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Dependencies tested in target environment
- [ ] Security review completed
- [ ] Performance testing done

### Production Deployment
```bash
# Docker deployment
docker-compose up -d

# Check deployment
docker-compose ps
docker-compose logs financial-analysis-app
```

## 📊 Code Architecture

### Core Components

#### `src/app.py`
- **web_search()**: DuckDuckGo integration
- **get_stock_data()**: Yahoo Finance data with 52-week & YTD
- **get_stock_news()**: News article retrieval
- **create_ui()**: Gradio interface creation

### Dependencies
- **gradio**: Web interface framework
- **yfinance**: Stock market data
- **ddgs**: Web search functionality
- **requests**: HTTP client
- **beautifulsoup4**: HTML parsing
- **pandas**: Data manipulation

### Configuration
- **Environment Variables**: `.env` file
- **Default Settings**: Hardcoded fallbacks
- **Port Configuration**: 7860 (configurable)

## 🔒 Security Considerations

### Input Validation
- Sanitize all user inputs
- Validate stock symbol formats
- Limit search query lengths
- Prevent injection attacks

### API Security
- No API keys stored in code
- Read-only access to external services
- Rate limiting considerations

### Data Privacy
- No user data persistence
- No logging of personal information
- Session-based data only

## 📈 Performance Optimization

### Code Optimization
- Efficient API calls
- Minimal dependencies
- Fast error handling
- Responsive UI design

### Caching Strategy
- Stock data caching (future enhancement)
- Search result optimization
- Browser resource management

## 🤝 Contributing Guidelines

### Code Standards
- Follow PEP 8 style guidelines
- Use descriptive variable names
- Add docstrings to all functions
- Include error handling

### Testing Requirements
- Unit tests for all new features
- E2E tests for UI changes
- Test coverage minimum 80%
- All tests must pass before merge

### Documentation Standards
- Update README for new features
- Add examples to documentation
- Keep API docs current
- Update testing guides

---

*This development guide provides comprehensive instructions for contributing to the Financial Analysis System.*
