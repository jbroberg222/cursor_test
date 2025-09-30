# Fancy Web Calculator

A beautiful, modern web-based calculator built with Python Flask and vanilla JavaScript. Features a sleek glassmorphism UI with smooth animations, responsive design, and comprehensive testing suite.

## 🚀 Quick Start

**Docker (Recommended):**
```bash
docker run -p 5001:5000 calculator-app
# Open http://localhost:5001
```

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

### **Advanced Calculator**
- 🔬 Scientific functions (sin, cos, tan, log, ln, sqrt, x², x!)
- 💾 Memory operations (MC, MR, M+, M-)
- 📐 Mathematical constants (π, e)
- 🎯 Utility functions (absolute value, negate)
- 📊 Side-by-side panel layout
- 🎛️ Mode switching between basic and advanced

### **Testing & Quality**
- ✅ Comprehensive unit test suite (26 tests, 24 passing)
- 📊 85% code coverage with detailed reporting
- 🔍 Error handling and validation
- 📝 Full documentation with JSDoc and docstrings
- 🛡️ Security-focused design with non-root Docker user
- 🐳 Docker containerization with health checks

## 📦 Installation

### **Option 1: Docker (Recommended)**

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

### **Option 2: Local Development**

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

## 🐳 Docker Commands

### **Build and Run**
```bash
# Build the Docker image
docker build -t calculator-app .

# Run the container
docker run -p 5001:5000 calculator-app

# Run with Docker Compose
docker-compose up --build
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
```

### **Current Docker Status**
- **Container Name**: `calculator-app`
- **Image**: `calculator-app:latest`
- **Port Mapping**: `0.0.0.0:5001->5000/tcp`
- **Status**: ✅ Running and accessible
- **URL**: `http://localhost:5001`
- **Health**: Container running (health check may show as starting)

**Quick Docker Commands:**
```bash
# Check running containers
docker ps

# View container logs
docker logs calculator-app

# Stop the container
docker stop calculator-app

# Remove the container
docker rm calculator-app
```

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
- **Total Tests**: 26
- **Passing**: 24 ✅
- **Failing**: 2 (minor error handling edge cases)
- **Code Coverage**: 85%
- **Test Categories**: Basic arithmetic, scientific functions, error handling, API endpoints

**Run Tests:**
```bash
# Run all tests with coverage
python3 -m pytest test_app.py --cov=app --cov-report=term-missing

# Run tests with verbose output
python3 -m pytest test_app.py -v
```

## Keyboard Shortcuts

- `0-9` and `.` - Number input
- `+`, `-`, `*`, `/` - Mathematical operations
- `Enter` or `=` - Calculate result
- `Escape` or `C` - Clear all
- `Backspace` - Delete last character

## 📁 Project Structure

```
cursor_test/
├── app.py                 # Flask application (documented)
├── test_app.py           # Unit tests (26 tests, 85% coverage)
├── run_tests.py          # Test runner script
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker container configuration
├── docker-compose.yml    # Docker Compose orchestration
├── .dockerignore         # Docker build context exclusions
├── README.md            # This documentation
├── templates/
│   └── calculator.html  # HTML template (documented)
└── static/
    ├── style.css        # CSS styles (documented)
    └── script.js        # JavaScript functionality (documented)
```

## 🔌 API Documentation

### **Basic Calculator Endpoint**
- **URL**: `/calculate`
- **Method**: `POST`
- **Content-Type**: `application/json`

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

## Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Custom CSS with glassmorphism effects
- **Fonts**: Google Fonts (Inter)

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## License

This project is open source and available under the MIT License.
