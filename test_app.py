"""
Unit tests for the Flask calculator application.

This module contains comprehensive tests for all calculator functionality including
basic arithmetic operations, scientific functions, error handling, and API endpoints.
"""

import unittest
import json
from app import app


class TestCalculatorApp(unittest.TestCase):
    """Test cases for the calculator Flask application."""
    
    def setUp(self):
        """Set up test client and configuration."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_index_route(self):
        """Test that the index route returns the calculator page."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'calculator', response.data.lower())
    
    def test_basic_addition(self):
        """Test basic addition operation."""
        response = self.app.post('/calculate', 
                               data=json.dumps({'expression': '2+3'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], '5')
    
    def test_basic_subtraction(self):
        """Test basic subtraction operation."""
        response = self.app.post('/calculate', 
                               data=json.dumps({'expression': '10-4'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], '6')
    
    def test_basic_multiplication(self):
        """Test basic multiplication operation."""
        response = self.app.post('/calculate', 
                               data=json.dumps({'expression': '3*4'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], '12')
    
    def test_basic_division(self):
        """Test basic division operation."""
        response = self.app.post('/calculate', 
                               data=json.dumps({'expression': '15/3'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], '5.0')
    
    def test_division_by_zero(self):
        """Test division by zero error handling."""
        response = self.app.post('/calculate', 
                               data=json.dumps({'expression': '5/0'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('Division by zero', data['error'])
    
    def test_complex_expression(self):
        """Test complex mathematical expression."""
        response = self.app.post('/calculate', 
                               data=json.dumps({'expression': '2+3*4-1'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], '13')
    
    def test_decimal_operations(self):
        """Test decimal number operations."""
        response = self.app.post('/calculate', 
                               data=json.dumps({'expression': '3.5+2.5'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], '6.0')
    
    def test_calculator_symbols(self):
        """Test calculator symbol conversion (× and ÷)."""
        response = self.app.post('/calculate', 
                               data=json.dumps({'expression': '3×4÷2'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], '6.0')
    
    def test_invalid_characters(self):
        """Test rejection of invalid characters."""
        response = self.app.post('/calculate', 
                               data=json.dumps({'expression': '2+3;DROP TABLE'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('Invalid characters', data['error'])
    
    def test_empty_expression(self):
        """Test empty expression handling."""
        response = self.app.post('/calculate', 
                               data=json.dumps({'expression': ''}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], '0')
    
    def test_invalid_expression(self):
        """Test invalid mathematical expression."""
        response = self.app.post('/calculate', 
                               data=json.dumps({'expression': '2++3'}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('Invalid expression', data['error'])


class TestScientificFunctions(unittest.TestCase):
    """Test cases for scientific calculator functions."""
    
    def setUp(self):
        """Set up test client and configuration."""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_sine_function(self):
        """Test sine function calculation."""
        response = self.app.post('/scientific', 
                               data=json.dumps({'function': 'sin', 'value': 30}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertAlmostEqual(float(data['result']), 0.5, places=1)
    
    def test_cosine_function(self):
        """Test cosine function calculation."""
        response = self.app.post('/scientific', 
                               data=json.dumps({'function': 'cos', 'value': 60}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertAlmostEqual(float(data['result']), 0.5, places=1)
    
    def test_tangent_function(self):
        """Test tangent function calculation."""
        response = self.app.post('/scientific', 
                               data=json.dumps({'function': 'tan', 'value': 45}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertAlmostEqual(float(data['result']), 1.0, places=1)
    
    def test_logarithm_function(self):
        """Test base-10 logarithm function."""
        response = self.app.post('/scientific', 
                               data=json.dumps({'function': 'log', 'value': 100}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], '2.0')
    
    def test_natural_logarithm_function(self):
        """Test natural logarithm function."""
        response = self.app.post('/scientific', 
                               data=json.dumps({'function': 'ln', 'value': 2.71828}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertAlmostEqual(float(data['result']), 1.0, places=1)
    
    def test_square_root_function(self):
        """Test square root function."""
        response = self.app.post('/scientific', 
                               data=json.dumps({'function': 'sqrt', 'value': 16}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], '4.0')
    
    def test_square_function(self):
        """Test square (power of 2) function."""
        response = self.app.post('/scientific', 
                               data=json.dumps({'function': 'pow', 'value': 5}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], '25.0')
    
    def test_factorial_function(self):
        """Test factorial function."""
        response = self.app.post('/scientific', 
                               data=json.dumps({'function': 'factorial', 'value': 5}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], '120')
    
    def test_absolute_value_function(self):
        """Test absolute value function."""
        response = self.app.post('/scientific', 
                               data=json.dumps({'function': 'abs', 'value': -5}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], '5.0')
    
    def test_negate_function(self):
        """Test negate function."""
        response = self.app.post('/scientific', 
                               data=json.dumps({'function': 'negate', 'value': 7}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['result'], '-7.0')
    
    def test_square_root_negative_number(self):
        """Test square root of negative number error."""
        response = self.app.post('/scientific', 
                               data=json.dumps({'function': 'sqrt', 'value': -4}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('Square root of negative number', data['error'])
    
    def test_logarithm_zero(self):
        """Test logarithm of zero error."""
        response = self.app.post('/scientific', 
                               data=json.dumps({'function': 'log', 'value': 0}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('Logarithm of non-positive number', data['error'])
    
    def test_factorial_negative(self):
        """Test factorial of negative number error."""
        response = self.app.post('/scientific', 
                               data=json.dumps({'function': 'factorial', 'value': -1}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('Invalid factorial input', data['error'])
    
    def test_unknown_function(self):
        """Test unknown function error."""
        response = self.app.post('/scientific', 
                               data=json.dumps({'function': 'unknown', 'value': 5}),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('Unknown function', data['error'])


if __name__ == '__main__':
    unittest.main()
