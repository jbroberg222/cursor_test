"""
Flask Calculator Application

A web-based calculator with basic arithmetic operations and advanced scientific functions.
Features a modern glassmorphism UI with both basic and advanced calculation modes.

Author: AI Assistant
Version: 1.0.0
License: MIT
"""

from flask import Flask, render_template, request, jsonify, g
import math
import cmath
import logging
import time
from expression_parser import safe_eval
from security import rate_limit, validate_json_input, InputValidator, add_security_headers
from cache import get_cache_manager, cached

# Initialize Flask application
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize cache manager
cache_manager = get_cache_manager()


@cached(cache_manager, ttl=3600)  # Cache for 1 hour
def cached_calculate(expression: str):
    """Cached calculation function."""
    return safe_eval(expression)


@cached(cache_manager, ttl=3600)  # Cache for 1 hour
def cached_scientific(function_name: str, value: float):
    """Cached scientific calculation function."""
    functions = {
        'sin': lambda x: math.sin(math.radians(x)),
        'cos': lambda x: math.cos(math.radians(x)),
        'tan': lambda x: math.tan(math.radians(x)),
        'log': lambda x: math.log10(x),
        'ln': lambda x: math.log(x),
        'sqrt': lambda x: math.sqrt(x),
        'pow': lambda x: x ** 2,
        'factorial': lambda x: math.factorial(int(x)) if x >= 0 and x == int(x) else None,
        'abs': lambda x: abs(x),
        'negate': lambda x: -x
    }
    
    return functions[function_name](value)


# Add security headers to all responses
@app.after_request
def after_request(response):
    return add_security_headers(response)

@app.route('/')
def index():
    """
    Render the main calculator page.
    
    Returns:
        str: Rendered HTML template for the calculator interface
    """
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
@rate_limit(max_requests=60, window_seconds=60)  # 60 requests per minute
@validate_json_input(['expression'])
def calculate():
    """
    Handle basic arithmetic calculations.
    
    Accepts mathematical expressions and returns calculated results.
    Supports basic operations: +, -, *, /, and parentheses.
    
    Args:
        JSON payload with 'expression' field containing mathematical expression
        
    Returns:
        JSON response with 'result' field containing calculation result
        or 'error' field with error message
        
    Example:
        POST /calculate
        {"expression": "2+3*4"}
        Response: {"result": "14"}
    """
    try:
        data = g.validated_data
        expression = data.get('expression', '')
        
        # Validate expression input
        is_valid, error_msg = InputValidator.validate_expression(expression)
        if not is_valid:
            logger.warning(f"Invalid expression input: {error_msg}")
            # For backward compatibility, return generic error for some cases
            if "Invalid characters" in error_msg:
                return jsonify({'error': 'Invalid characters in expression'}), 400
            return jsonify({'error': error_msg}), 400
        
        # Replace common calculator symbols first
        expression = expression.replace('×', '*').replace('÷', '/')
        
        # Log the calculation attempt
        logger.info(f"Calculating expression: {expression}")
        
        # Evaluate the expression safely using our cached parser
        result = cached_calculate(expression)
        
        # Handle special cases
        if isinstance(result, float):
            if result == float('inf') or result == float('-inf'):
                return jsonify({'error': 'Infinity'}), 400
            if math.isnan(result):
                return jsonify({'error': 'Not a number'}), 400
            # Round to avoid floating point precision issues
            result = round(result, 10)
            # Format as integer if it's a whole number
            if result.is_integer():
                result = int(result)
        
        return jsonify({'result': str(result)})
    
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero'}), 400
    except Exception as e:
        return jsonify({'error': 'Invalid expression'}), 400

@app.route('/scientific', methods=['POST'])
@rate_limit(max_requests=60, window_seconds=60)  # 60 requests per minute
@validate_json_input(['function', 'value'])
def scientific():
    """
    Handle scientific calculator functions.
    
    Provides advanced mathematical functions including trigonometric,
    logarithmic, and other scientific operations.
    
    Args:
        JSON payload with:
        - 'function': Name of the scientific function to apply
        - 'value': Numeric value to apply the function to
        
    Returns:
        JSON response with 'result' field containing calculation result
        or 'error' field with error message
        
    Supported Functions:
        - sin, cos, tan: Trigonometric functions (input in degrees)
        - log: Base-10 logarithm
        - ln: Natural logarithm
        - sqrt: Square root
        - pow: Square (x²)
        - factorial: Factorial function
        - abs: Absolute value
        - negate: Negate value (multiply by -1)
        
    Example:
        POST /scientific
        {"function": "sin", "value": 30}
        Response: {"result": "0.5"}
    """
    try:
        data = g.validated_data
        function_name = data.get('function')
        value = float(data.get('value', 0))
        
        # Validate scientific function input
        is_valid, error_msg = InputValidator.validate_scientific_input(function_name, value)
        if not is_valid:
            logger.warning(f"Invalid scientific function input: {error_msg}")
            return jsonify({'error': error_msg}), 400
        
        # Log the scientific calculation attempt
        logger.info(f"Scientific calculation: {function_name}({value})")
        
        # Validate function name
        valid_functions = ['sin', 'cos', 'tan', 'log', 'ln', 'sqrt', 'pow', 'factorial', 'abs', 'negate']
        if function_name not in valid_functions:
            return jsonify({'error': 'Unknown function'}), 400
        
        # Special validation for certain functions
        if function_name == 'sqrt' and value < 0:
            return jsonify({'error': 'Square root of negative number'}), 400
        if function_name == 'log' and value <= 0:
            return jsonify({'error': 'Logarithm of non-positive number'}), 400
        if function_name == 'ln' and value <= 0:
            return jsonify({'error': 'Natural log of non-positive number'}), 400
        if function_name == 'factorial' and (value < 0 or value != int(value) or value > 170):
            return jsonify({'error': 'Invalid factorial input'}), 400
        
        # Use cached scientific calculation
        result = cached_scientific(function_name, value)
        
        if result is None:
            return jsonify({'error': 'Invalid calculation'}), 400
        
        # Handle special cases
        if isinstance(result, float):
            if result == float('inf') or result == float('-inf'):
                return jsonify({'error': 'Infinity'}), 400
            if math.isnan(result):
                return jsonify({'error': 'Not a number'}), 400
            # Round to avoid floating point precision issues
            result = round(result, 10)
        
        return jsonify({'result': str(result)})
    
    except Exception as e:
        logger.error(f"Scientific calculation error: {str(e)}")
        return jsonify({'error': 'Calculation error'}), 400


@app.route('/health')
def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns:
        JSON response with service status
    """
    return jsonify({
        'status': 'healthy',
        'service': 'calculator',
        'version': '1.0.0',
        'timestamp': time.time()
    })


@app.route('/metrics')
def metrics():
    """
    Basic metrics endpoint for monitoring.
    
    Returns:
        JSON response with basic metrics
    """
    return jsonify({
        'uptime': time.time() - app.start_time if hasattr(app, 'start_time') else 0,
        'requests_total': getattr(app, 'request_count', 0),
        'errors_total': getattr(app, 'error_count', 0)
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(429)
def rate_limit_exceeded(error):
    """Handle rate limit exceeded errors."""
    return jsonify({'error': 'Rate limit exceeded'}), 429


if __name__ == '__main__':
    # Set start time for metrics
    app.start_time = time.time()
    app.request_count = 0
    app.error_count = 0
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)
