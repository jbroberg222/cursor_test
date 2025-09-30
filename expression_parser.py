"""
Safe Mathematical Expression Parser

A secure alternative to eval() for parsing mathematical expressions.
Supports basic arithmetic operations with proper validation and error handling.
"""

import re
import math
from typing import Union, List, Tuple


class SafeExpressionParser:
    """
    A safe mathematical expression parser that replaces eval() functionality.
    
    Supports:
    - Basic arithmetic: +, -, *, /
    - Parentheses grouping
    - Decimal numbers
    - Scientific notation (e, E)
    - Proper error handling and validation
    """
    
    def __init__(self):
        # Define allowed tokens
        self.number_pattern = r'\d+\.?\d*(?:[eE][+-]?\d+)?'
        self.operator_pattern = r'[+\-*/]'
        self.parenthesis_pattern = r'[()]'
        
        # Compile regex patterns
        self.number_regex = re.compile(self.number_pattern)
        self.token_regex = re.compile(
            f'({self.number_pattern}|{self.operator_pattern}|{self.parenthesis_pattern})'
        )
    
    def parse(self, expression: str) -> Union[float, int]:
        """
        Parse and evaluate a mathematical expression safely.
        
        Args:
            expression: Mathematical expression string
            
        Returns:
            Calculated result as float or int
            
        Raises:
            ValueError: If expression is invalid or contains unsafe operations
            ZeroDivisionError: If division by zero occurs
        """
        if not expression or not expression.strip():
            raise ValueError("Empty expression")
        
        # Clean and validate expression
        expression = expression.strip()
        self._validate_expression(expression)
        
        # Tokenize the expression
        tokens = self._tokenize(expression)
        
        # Convert to postfix notation (RPN)
        postfix = self._infix_to_postfix(tokens)
        
        # Evaluate postfix expression
        result = self._evaluate_postfix(postfix)
        
        return result
    
    def _validate_expression(self, expression: str) -> None:
        """Validate expression for security and syntax."""
        # Check length limit
        if len(expression) > 1000:
            raise ValueError("Expression too long")
        
        # Check for allowed characters only
        allowed_chars = set('0123456789+-*/.()eE ')
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Invalid characters in expression")
        
        # Check for balanced parentheses
        if not self._balanced_parentheses(expression):
            raise ValueError("Unbalanced parentheses")
        
        # Check for consecutive operators
        if re.search(r'[+\-*/]{2,}', expression):
            raise ValueError("Consecutive operators not allowed")
        
        # Check for operators at start/end (except minus for negative numbers)
        if expression[0] in '+*/' or expression[-1] in '+-*/':
            raise ValueError("Invalid operator placement")
    
    def _balanced_parentheses(self, expression: str) -> bool:
        """Check if parentheses are balanced."""
        count = 0
        for char in expression:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
                if count < 0:
                    return False
        return count == 0
    
    def _tokenize(self, expression: str) -> List[str]:
        """Tokenize expression into numbers, operators, and parentheses."""
        # Remove spaces
        expression = expression.replace(' ', '')
        
        # Find all tokens
        tokens = self.token_regex.findall(expression)
        
        if not tokens:
            raise ValueError("No valid tokens found")
        
        # Validate token sequence
        self._validate_token_sequence(tokens)
        
        return tokens
    
    def _validate_token_sequence(self, tokens: List[str]) -> None:
        """Validate the sequence of tokens."""
        operators = set('+-*/')
        parentheses = set('()')
        
        for i, token in enumerate(tokens):
            if token in operators:
                # Check for valid operator context
                if i == 0 and token != '-':  # Only minus allowed at start
                    raise ValueError("Invalid operator at start")
                if i == len(tokens) - 1:
                    raise ValueError("Operator at end of expression")
            elif token in parentheses:
                continue
            elif not self._is_number(token):
                raise ValueError(f"Invalid token: {token}")
    
    def _is_number(self, token: str) -> bool:
        """Check if token is a valid number."""
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    def _infix_to_postfix(self, tokens: List[str]) -> List[str]:
        """Convert infix notation to postfix (RPN) notation."""
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
        output = []
        operators = []
        
        for token in tokens:
            if self._is_number(token):
                output.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                if operators:
                    operators.pop()  # Remove '('
            elif token in precedence:
                while (operators and operators[-1] != '(' and 
                       precedence[operators[-1]] >= precedence[token]):
                    output.append(operators.pop())
                operators.append(token)
        
        while operators:
            output.append(operators.pop())
        
        return output
    
    def _evaluate_postfix(self, postfix: List[str]) -> Union[float, int]:
        """Evaluate postfix expression."""
        stack = []
        
        for token in postfix:
            if self._is_number(token):
                stack.append(float(token))
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid expression")
                
                b = stack.pop()
                a = stack.pop()
                
                if token == '+':
                    result = a + b
                elif token == '-':
                    result = a - b
                elif token == '*':
                    result = a * b
                elif token == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    result = a / b
                else:
                    raise ValueError(f"Unknown operator: {token}")
                
                stack.append(result)
        
        if len(stack) != 1:
            raise ValueError("Invalid expression")
        
        result = stack[0]
        
        # Handle special cases
        if math.isinf(result):
            raise ValueError("Result is infinity")
        if math.isnan(result):
            raise ValueError("Result is not a number")
        
        # Always return float for consistency with original behavior
        return float(result)


# Global parser instance
_parser = SafeExpressionParser()


def safe_eval(expression: str) -> Union[float, int]:
    """
    Safe alternative to eval() for mathematical expressions.
    
    Args:
        expression: Mathematical expression string
        
    Returns:
        Calculated result
        
    Raises:
        ValueError: If expression is invalid
        ZeroDivisionError: If division by zero occurs
    """
    return _parser.parse(expression)
