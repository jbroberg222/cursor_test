"""
Flask Calculator Application

A web-based calculator with basic arithmetic operations and advanced scientific functions.
Features a modern glassmorphism UI with both basic and advanced calculation modes.

Author: AI Assistant
Version: 1.0.0
License: MIT
"""

from flask import Flask, render_template, request, jsonify
import math
import cmath

# Initialize Flask application
app = Flask(__name__)

@app.route('/')
def index():
    """
    Render the main calculator page.
    
    Returns:
        str: Rendered HTML template for the calculator interface
    """
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
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
        data = request.get_json()
        expression = data.get('expression', '')
        
        # Replace common calculator symbols first
        expression = expression.replace('×', '*').replace('÷', '/')
        
        # Security: Only allow safe mathematical operations
        allowed_chars = set('0123456789+-*/.()eE ')
        if not all(c in allowed_chars for c in expression):
            return jsonify({'error': 'Invalid characters in expression'}), 400
        
        # Evaluate the expression safely
        result = eval(expression)
        
        # Handle special cases
        if isinstance(result, float):
            if result == float('inf') or result == float('-inf'):
                return jsonify({'error': 'Infinity'}), 400
            if math.isnan(result):
                return jsonify({'error': 'Not a number'}), 400
            # Round to avoid floating point precision issues
            result = round(result, 10)
        
        return jsonify({'result': str(result)})
    
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero'}), 400
    except Exception as e:
        return jsonify({'error': 'Invalid expression'}), 400

@app.route('/scientific', methods=['POST'])
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
        data = request.get_json()
        function_name = data.get('function')
        value = float(data.get('value', 0))
        
        # Scientific functions dictionary
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
        
        if function_name not in functions:
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
        
        result = functions[function_name](value)
        
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
        return jsonify({'error': 'Calculation error'}), 400

if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)
