# Fancy Web Calculator

A beautiful, modern web-based calculator built with Python Flask and vanilla JavaScript. Features a sleek glassmorphism UI with smooth animations, responsive design, comprehensive testing suite, enterprise-grade security, and production-ready performance optimizations.

## 🚀 Quick Start

**Docker (Recommended):**
```bash
docker run -p 5001:5000 calculator-app
# Open http://localhost:5001
```

**Note**: Port 5000 is used by macOS AirPlay Receiver, so we use port 5001 for local access.

**Local Development:**
```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

## 🚀 Features

### **Basic Calculator**
- ✨ Modern glassmorphism design with gradient backgrounds
- 🎨 Smooth animations and hover effects
- 📱 Fully responsive design for mobile and desktop
- ⌨️ Full keyboard support
- 🔢 Basic arithmetic operations (+, -, ×, ÷)
- 🧮 Clear, Clear Entry, and Backspace functions
- 🚀 Server-side calculation for accuracy
- ⚡ Real-time display updates
- 🕒 **Live timestamp** with date and time display above mode toggle

### **Advanced Calculator**
- 🔬 Scientific functions (sin, cos, tan, log, ln, sqrt, x², x!)
- 💾 Memory operations (MC, MR, M+, M-)
- 📐 Mathematical constants (π, e)
- 🎯 Utility functions (absolute value, negate)
- 📊 Side-by-side panel layout
- 🎛️ Mode switching between basic and advanced

### **Security & Performance**
- 🛡️ **Enterprise Security**: Safe expression parser (no eval() vulnerabilities)
- 🚫 **Rate Limiting**: 60 requests/minute per IP with DoS protection
- 🔒 **Input Validation**: Comprehensive sanitization and pattern detection
- ⚡ **High Performance**: Redis + in-memory caching (~90% faster for repeated calculations)
- 🏭 **Production Ready**: Gunicorn WSGI server with optimized Docker containers
- 📊 **Monitoring**: Health checks, metrics endpoints, and structured logging

### **Testing & Quality**
- ✅ Comprehensive unit test suite (34 tests, 34 passing)
- 📊 84% code coverage with detailed reporting
- 🔍 Advanced error handling and validation
- 📝 Full documentation with JSDoc and docstrings
- 🛡️ Security-focused design with non-root Docker user
- 🐳 Docker containerization with health checks
- 🚫 **Pre-commit Hooks**: Automatic test execution before commits (blocks if >10% tests fail)
- 🧪 **Test Categories**: Basic arithmetic, scientific functions, security, caching, health checks, error handling

## 📦 Installation

### **Option 1: Production Docker (Recommended)**

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd cursor_test
   ```

2. **Run production deployment with Redis caching**
   ```bash
   docker-compose -f docker-compose.prod.yml up --build
   ```

3. **Open your browser and navigate to**
   ```
   http://localhost:5000
   ```

### **Option 2: Development Docker**

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd cursor_test
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Open your browser and navigate to**
   ```
   http://localhost:5000
   ```

### **Option 3: Local Development**

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd cursor_test
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser and navigate to**
   ```
   http://127.0.0.1:5000
   ```

## 🛡️ Security Features

### **Enterprise-Grade Security**
- **Safe Expression Parser**: Replaced dangerous `eval()` with custom parser
- **Rate Limiting**: 60 requests/minute per IP address
- **Input Validation**: Comprehensive sanitization and pattern detection
- **Security Headers**: CSP, HSTS, XSS protection, and more
- **DoS Protection**: Automatic blocking of suspicious patterns

### **Monitoring & Health Checks**
- **Health Endpoint**: `GET /health` - Service status for load balancers
- **Metrics Endpoint**: `GET /metrics` - Performance and usage statistics
- **Structured Logging**: Comprehensive logging with proper log levels
- **Error Tracking**: Detailed error reporting and metrics

## 🐳 Docker Commands

### **Production Deployment**
```bash
# Production with Redis caching
docker-compose -f docker-compose.prod.yml up --build

# Production Docker image (multi-stage build)
docker build -f Dockerfile.prod -t calculator-app-prod .
docker run -p 5000:5000 calculator-app-prod

# Production with resource limits and logging
docker-compose -f docker-compose.prod.yml up -d --build
```

**Production Features:**
- **Multi-stage build** for optimized image size
- **Gunicorn WSGI server** with 4 workers
- **Redis caching** with persistence
- **Resource limits**: 512MB RAM, 0.5 CPU
- **Logging**: JSON format with rotation
- **Health checks**: `/health` endpoint monitoring
- **Security**: Non-root user execution

### **Development Deployment**
```bash
# Build the Docker image
docker build -t calculator-app .

# Run the container (using port 5001 to avoid macOS AirPlay conflict)
docker run -p 5001:5000 calculator-app

# Run with Docker Compose
docker-compose up --build

# Check container status
docker ps
```

### **Development with Docker**
```bash
# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down

# Rebuild after changes
docker-compose up --build --force-recreate
```

### **Docker Health Check**
The container includes a health check that monitors the application:
```bash
# Check container health
docker ps

# View health check logs
docker inspect calculator-app

# View container logs
docker logs calculator-app
```

**Health Check Configuration:**
- **Development**: Checks `http://localhost:5000/` every 30s
- **Production**: Checks `http://localhost:5000/health` every 30s
- **Timeout**: 10s
- **Retries**: 3 attempts
- **Start Period**: 40s (allows app startup time)

### **Current Docker Status**
- **Container Name**: `calculator-app`
- **Image**: `calculator-app:latest` (310MB)
- **Port Mapping**: `0.0.0.0:5001->5000/tcp`
- **Status**: ⏸️ Stopped (last run 7 minutes ago)
- **URL**: `http://localhost:5001` (when running)
- **Health**: Health check configured for `/health` endpoint

**Quick Docker Commands:**
```bash
# Check running containers
docker ps

# Check all containers (including stopped)
docker ps -a

# View container logs
docker logs calculator-app

# Start the container
docker start calculator-app

# Stop the container
docker stop calculator-app

# Remove the container
docker rm calculator-app

# Remove the image
docker rmi calculator-app

# View image details
docker images calculator-app
```

### **Docker Images Available**
- **calculator-app:latest** (310MB) - Development image
- **cursor_test-calculator:latest** (310MB) - Docker Compose image
- **calculator-app-prod** - Production image (when built)

### **Port Configuration**
- **Container Internal Port**: 5000
- **Host Port**: 5001 (to avoid macOS AirPlay Receiver conflict on 5000)
- **Access URL**: `http://localhost:5001`
- **Production**: Uses port 5000 internally with Gunicorn WSGI server

## 🚀 Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:5000` (local) or `http://localhost:5001` (Docker)

3. **Start calculating!**
   - Use mouse clicks or keyboard input
   - Press `C` or `Escape` to clear all
   - Press `CE` to clear entry
   - Press `⌫` or `Backspace` to delete last character

## 🧪 Testing

### **Run All Tests**
```bash
python run_tests.py
```

### **Run Tests with Coverage**
```bash
pytest --cov=app --cov-report=html
```

### **Run Specific Test Categories**
```bash
# Basic arithmetic tests only
python -m unittest test_app.TestCalculatorApp

# Scientific function tests only
python -m unittest test_app.TestScientificFunctions
```

### **Test Coverage Report**
After running tests with coverage, open `htmlcov/index.html` in your browser to view detailed coverage reports.

### **Current Test Status**
- **Total Tests**: 34
- **Passing**: 34 ✅
- **Failing**: 0 (0% failure rate - commits allowed)
- **Code Coverage**: 84%
- **Test Categories**: 
  - Basic arithmetic operations (8 tests)
  - Scientific functions (13 tests)
  - Health & metrics endpoints (2 tests)
  - Error handling (1 test)
  - Security features (3 tests)
  - Caching functionality (2 tests)
  - API endpoints (5 tests)

**Run Tests:**
```bash
# Run all tests with coverage
python3 -m pytest test_app.py --cov=app --cov-report=term-missing

# Run tests with verbose output
python3 -m pytest test_app.py -v

# Run specific test categories
python3 -m pytest test_app.py::TestCalculatorApp -v  # Basic arithmetic
python3 -m pytest test_app.py::TestScientificFunctions -v  # Scientific functions
python3 -m pytest test_app.py::TestHealthAndMetrics -v  # Health & metrics
python3 -m pytest test_app.py::TestSecurityFeatures -v  # Security features
python3 -m pytest test_app.py::TestCachingFeatures -v  # Caching features
python3 -m pytest test_app.py::TestErrorHandlers -v  # Error handling
```

### **Test Categories Breakdown**

#### **🧮 Basic Arithmetic Tests (8 tests)**
- Addition, subtraction, multiplication, division
- Complex expressions with parentheses
- Decimal operations
- Calculator symbol conversion (×, ÷)
- Division by zero handling
- Invalid character detection
- Empty expression handling

#### **🔬 Scientific Function Tests (13 tests)**
- Trigonometric functions (sin, cos, tan)
- Logarithmic functions (log, ln)
- Square root and power functions
- Factorial calculations
- Absolute value and negation
- Error handling for invalid inputs
- Edge cases (negative numbers, zero, large values)

#### **🏥 Health & Metrics Tests (2 tests)**
- Health check endpoint (`/health`)
- Metrics endpoint (`/metrics`)
- Service status validation
- Performance metrics collection

#### **🛡️ Security Feature Tests (3 tests)**
- Input validation for missing fields
- Invalid JSON handling
- Non-JSON request rejection
- Content-Type validation

#### **⚡ Caching Tests (2 tests)**
- Calculation result caching
- Scientific function result caching
- Cache hit/miss validation

#### **❌ Error Handling Tests (1 test)**
- 404 error handling
- Proper error message formatting

### **Pre-commit Hooks**
Automatically run tests before each commit to maintain code quality:

```bash
# Check hook status
./setup-pre-commit.sh status

# Enable basic hook (10% failure threshold)
./setup-pre-commit.sh basic

# Enable advanced hook (with coverage)
./setup-pre-commit.sh advanced

# Disable hook temporarily
./setup-pre-commit.sh disable
```

**Hook Behavior:**
- ✅ **Commits allowed** if ≤10% of tests fail
- ❌ **Commits blocked** if >10% of tests fail
- 📊 **Detailed reporting** with test counts and failure rates
- 🔧 **Helpful error messages** with fix suggestions

**Bypass (Not Recommended):**
```bash
git commit --no-verify -m "Emergency fix"
```

## 🔍 Static Code Analysis Pipeline

The project now includes comprehensive static code analysis tools that run automatically before each commit:

### **Analysis Tools:**
- **📝 Flake8**: Code style and linting (PEP 8 compliance)
- **🔒 Bandit**: Security vulnerability scanning
- **🔍 MyPy**: Type checking and static analysis

### **Configuration:**
- **`.flake8`**: Flake8 configuration with lenient rules for development
- **`.bandit`**: Bandit configuration skipping common false positives
- **`mypy.ini`**: MyPy configuration with relaxed type checking

### **Pre-commit Integration:**
- **✅ Automatic**: Runs on every commit attempt
- **⚠️ Non-blocking**: Issues are warnings, not commit blockers
- **📊 Reporting**: Detailed output for each analysis tool
- **🔄 Version Increment**: Still includes automatic version bumping
- **📚 README Check**: Ensures documentation is updated with meaningful changes

### **Usage:**
```bash
# Run analysis tools manually
python3 -m flake8 . --count --statistics
python3 -m bandit -r . -f txt
python3 -m mypy . --no-error-summary

# Commit with analysis (automatic)
git commit -m "your commit message"
```

## 🕒 Live Timestamp Feature

The calculator includes a live timestamp display that shows the current date and time:

### **Features:**
- ✅ **Real-time updates** every second
- ✅ **Format**: "Day - mm/dd/yy hh:mm:ss AM/PM" (e.g., "Monday - 09/30/24 09:15:30 PM")
- ✅ **Location**: Above the Basic/Advanced mode toggle buttons
- ✅ **Styling**: Glassmorphism design matching the calculator theme
- ✅ **Responsive**: Works on all screen sizes

### **Technical Details:**
- **JavaScript**: Updates every 1000ms using `setInterval()`
- **Formatting**: Custom date/time formatting with proper padding
- **Initialization**: Automatically starts when page loads
- **Performance**: Lightweight with minimal CPU usage

## Keyboard Shortcuts

- `0-9` and `.` - Number input
- `+`, `-`, `*`, `/` - Mathematical operations
- `Enter` or `=` - Calculate result
- `Escape` or `C` - Clear all
- `Backspace` - Delete last character

## 📁 Project Structure

```
cursor_test/
├── app.py                    # Flask application with security & caching
├── test_app.py              # Unit tests (34 tests, 84% coverage)
├── run_tests.py             # Test runner script
├── requirements.txt         # Python dependencies (including Redis)
├── Dockerfile               # Development Docker container
├── Dockerfile.prod          # Production-optimized container
├── docker-compose.yml       # Development Docker Compose
├── docker-compose.prod.yml  # Production deployment with Redis
├── .dockerignore            # Docker build context exclusions
├── .gitignore               # Git ignore patterns
├── README.md               # This comprehensive documentation
├── PRE-COMMIT-HOOKS.md     # Pre-commit hook documentation
├── setup-pre-commit.sh     # Pre-commit hook management script
├── expression_parser.py     # Safe mathematical expression parser
├── security.py             # Input validation & rate limiting
├── cache.py                # Redis + memory caching system
├── .git/hooks/             # Git pre-commit hooks
│   ├── pre-commit          # Basic hook (10% failure threshold)
│   ├── pre-commit-advanced # Advanced hook (with coverage)
│   └── pre-commit-config   # Hook configuration
├── templates/
│   └── calculator.html     # HTML template with timestamp & version
└── static/
    ├── style.css           # CSS styles with glassmorphism & responsive design
    └── script.js           # JavaScript with live timestamp & version dialog
```

## 🔌 API Documentation

### **Basic Calculator Endpoint**
- **URL**: `/calculate`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Rate Limit**: 60 requests/minute per IP

**Request Body:**
```json
{
    "expression": "2+3*4"
}
```

**Response:**
```json
{
    "result": "14"
}
```

**Error Response:**
```json
{
    "error": "Division by zero"
}
```

### **Scientific Functions Endpoint**
- **URL**: `/scientific`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Rate Limit**: 60 requests/minute per IP

**Request Body:**
```json
{
    "function": "sin",
    "value": 30
}
```

**Response:**
```json
{
    "result": "0.5"
}
```

**Supported Functions:**
- `sin`, `cos`, `tan` - Trigonometric functions (degrees)
- `log` - Base-10 logarithm
- `ln` - Natural logarithm
- `sqrt` - Square root
- `pow` - Square (x²)
- `factorial` - Factorial function
- `abs` - Absolute value
- `negate` - Negate value

### **Health Check Endpoint**
- **URL**: `/health`
- **Method**: `GET`
- **Purpose**: Service health monitoring for load balancers

**Response:**
```json
{
    "status": "healthy",
    "service": "calculator",
    "version": "1.0.0",
    "timestamp": 1696123456.789
}
```

### **Metrics Endpoint**
- **URL**: `/metrics`
- **Method**: `GET`
- **Purpose**: Performance and usage statistics

**Response:**
```json
{
    "uptime": 3600.5,
    "requests_total": 1250,
    "errors_total": 5
}
```

## 📋 Version Information

### **Current Version: v 0.18**
- **Release Date**: September 30, 2025, 2025, 2025, 2025, 2025, 2025, 2025, 2025, 2025, 2025, 2025, 2025, 2024
- **Status**: Stable Production Release
- **Compatibility**: Python 3.8+, Modern Browsers

### **Version History**
- **v 0.5** (Current) - Added live timestamp, version dialog, comprehensive testing
- **v 0.4** - Added pre-commit hooks, security enhancements, caching system
- **v 0.3** - Added advanced calculator mode, scientific functions, memory operations
- **v 0.2** - Added Docker containerization, production deployment
- **v 0.1** - Initial release with basic calculator functionality

### **Changelog**
#### **v 0.5 Features:**
- ✅ Live timestamp display with real-time updates
- ✅ Version dialog with attribution information
- ✅ Comprehensive test suite (34 tests, 84% coverage)
- ✅ Enhanced security testing and validation
- ✅ Caching functionality testing
- ✅ Health check and metrics endpoint testing
- ✅ Error handling improvements
- ✅ Updated documentation and README

## Technologies Used

- **Backend**: Python Flask with Gunicorn WSGI server
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with glassmorphism effects
- **Caching**: Redis + in-memory caching system
- **Security**: Custom expression parser, rate limiting, input validation
- **Monitoring**: Health checks, metrics endpoints, structured logging
- **Deployment**: Docker with multi-stage builds, Docker Compose
- **Testing**: pytest with coverage reporting
- **Fonts**: Google Fonts (Inter)
- **Version Control**: Git with pre-commit hooks

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## License

This project is open source and available under the MIT License.
# Static Code Analysis Pipeline Added

## 📚 README Documentation Check

This project now includes a pre-commit check to ensure the README is updated with meaningful documentation for each commit.

### **Features:**
- **✅ Automatic Check**: Verifies README.md is modified in each commit
- **📝 Content Analysis**: Distinguishes between meaningful changes and auto-generated version updates
- **⚠️ Smart Warnings**: Warns when only version changes are present but allows commits to proceed
- **🔧 Helpful Guidance**: Provides suggestions for what to document

### **Check Behavior:**
- **✅ Meaningful Changes**: Commits with substantial README updates pass without warnings
- **⚠️ Version-Only Changes**: Commits with only auto-generated version updates show warnings but proceed
- **❌ No README Changes**: Commits without README updates are blocked with helpful instructions

### **What to Document:**
- **🆕 New Features**: Describe new functionality and how to use it
- **⚙️ Configuration Changes**: Document setup or configuration modifications
- **🚨 Breaking Changes**: Note any changes that might affect existing users
- **📖 Usage Examples**: Add examples or improved instructions
- **🔧 Bug Fixes**: Document important fixes and their impact
# Final test of complete pre-commit pipeline
