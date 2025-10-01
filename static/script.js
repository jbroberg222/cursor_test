/**
 * Calculator JavaScript Module
 * 
 * Provides client-side functionality for the web-based calculator application.
 * Handles basic arithmetic operations, scientific functions, memory operations,
 * and UI interactions including mode switching and keyboard support.
 * 
 * @author AI Assistant
 * @version 1.0.0
 * @license MIT
 */

// Global calculator state variables
let display = document.getElementById('display');
let currentInput = '0';
let operator = null;
let previousInput = null;
let shouldResetDisplay = false;
let memoryValue = 0;
let isAdvancedMode = false;

/**
 * Updates the live timestamp display.
 * Formats the current date and time in "Day - mm/dd/yy hh:mm:ss AM/PM" format.
 */
function updateTimestamp() {
    const timestampElement = document.getElementById('timestamp');
    if (timestampElement) {
        const now = new Date();
        const dayOptions = { weekday: 'long' };
        const day = now.toLocaleDateString('en-US', dayOptions);
        
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const dayNum = String(now.getDate()).padStart(2, '0');
        const year = String(now.getFullYear()).slice(-2);
        
        const hours = String(now.getHours() % 12 || 12).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const seconds = String(now.getSeconds()).padStart(2, '0');
        const ampm = now.getHours() >= 12 ? 'PM' : 'AM';
        
        timestampElement.textContent = `${day} - ${month}/${dayNum}/${year} ${hours}:${minutes}:${seconds} ${ampm}`;
    }
}

/**
 * Initializes the timestamp and sets up automatic updates.
 * Updates every second to show live time.
 */
function initializeTimestamp() {
    updateTimestamp(); // Initial update
    setInterval(updateTimestamp, 1000); // Update every second
}

/**
 * Updates the calculator display with the current input value.
 */
function updateDisplay() {
    display.textContent = currentInput;
}

/**
 * Clears all calculator state and resets to initial state.
 * Clears current input, operator, previous input, and resets display flag.
 */
function clearAll() {
    currentInput = '0';
    operator = null;
    previousInput = null;
    shouldResetDisplay = false;
    updateDisplay();
}

/**
 * Clears only the current entry, leaving operator and previous input intact.
 */
function clearEntry() {
    currentInput = '0';
    updateDisplay();
}

/**
 * Removes the last character from the current input.
 * If only one character remains, resets to '0'.
 */
function backspace() {
    if (currentInput.length > 1) {
        currentInput = currentInput.slice(0, -1);
    } else {
        currentInput = '0';
    }
    updateDisplay();
}

/**
 * Appends a character to the current input.
 * Handles special cases like decimal points and leading zeros.
 * 
 * @param {string} value - The character to append to the display
 */
function appendToDisplay(value) {
    if (shouldResetDisplay) {
        currentInput = '0';
        shouldResetDisplay = false;
    }
    
    if (value === '.' && currentInput.includes('.')) {
        return; // Prevent multiple decimal points
    }
    
    if (currentInput === '0' && value !== '.') {
        currentInput = value;
    } else {
        currentInput += value;
    }
    
    updateDisplay();
}

/**
 * Sets the operator for the next calculation.
 * If an operator is already set, performs the calculation first.
 * 
 * @param {string} op - The operator symbol (+, -, ×, ÷)
 */
function setOperator(op) {
    if (operator && previousInput !== null) {
        calculate();
    }
    
    operator = op;
    previousInput = currentInput;
    shouldResetDisplay = true;
}

/**
 * Performs the calculation using the stored operator and operands.
 * Handles basic arithmetic operations with proper error checking.
 */
function calculate() {
    if (operator && previousInput !== null) {
        const prev = parseFloat(previousInput);
        const current = parseFloat(currentInput);
        let result;
        
        switch (operator) {
            case '+':
                result = prev + current;
                break;
            case '-':
                result = prev - current;
                break;
            case '×':
                result = prev * current;
                break;
            case '÷':
                if (current === 0) {
                    showError('Division by zero');
                    return;
                }
                result = prev / current;
                break;
            default:
                return;
        }
        
        // Round to avoid floating point precision issues
        result = Math.round(result * 10000000000) / 10000000000;
        
        currentInput = result.toString();
        operator = null;
        previousInput = null;
        shouldResetDisplay = true;
        updateDisplay();
    }
}

/**
 * Enhanced calculate function that sends calculations to the server.
 * Provides server-side calculation with loading states and error handling.
 */
async function calculateServer() {
    // Don't calculate if there's no meaningful input
    if (currentInput === '0' && !operator && !previousInput) {
        return;
    }
    
    try {
        // Show loading state
        const equalsBtn = document.querySelector('.btn-equals');
        equalsBtn.classList.add('loading');
        
        // Build the complete expression
        let expression = currentInput;
        if (operator && previousInput !== null) {
            expression = previousInput + operator + currentInput;
        }
        
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ expression: expression })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentInput = data.result;
            operator = null;
            previousInput = null;
            shouldResetDisplay = true;
            updateDisplay();
        } else {
            showError(data.error);
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError('Network error');
    } finally {
        // Remove loading state
        const equalsBtn = document.querySelector('.btn-equals');
        equalsBtn.classList.remove('loading');
    }
}

/**
 * Displays an error message on the calculator display.
 * Shows the error for 2 seconds then resets the calculator.
 * 
 * @param {string} message - The error message to display
 */
function showError(message) {
    display.textContent = message;
    display.classList.add('error');
    
    setTimeout(() => {
        display.classList.remove('error');
        currentInput = '0';
        operator = null;
        previousInput = null;
        shouldResetDisplay = false;
        updateDisplay();
    }, 2000);
}

// Keyboard support
document.addEventListener('keydown', function(event) {
    const key = event.key;
    
    if (key >= '0' && key <= '9' || key === '.') {
        appendToDisplay(key);
    } else if (key === '+' || key === '-') {
        setOperator(key);
    } else if (key === '*') {
        setOperator('×');
    } else if (key === '/') {
        event.preventDefault();
        setOperator('÷');
    } else if (key === 'Enter' || key === '=') {
        event.preventDefault();
        calculateServer();
    } else if (key === 'Escape' || key === 'c' || key === 'C') {
        clearAll();
    } else if (key === 'Backspace') {
        backspace();
    }
});

// Update button click handlers to use server calculation
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the live timestamp
    initializeTimestamp();
    
    // Override the calculate function for the equals button
    const equalsBtn = document.querySelector('.btn-equals');
    equalsBtn.onclick = calculateServer;
    
    // Operator handlers are now set directly in HTML onclick attributes
});

/**
 * ADVANCED MODE FUNCTIONS
 */

/**
 * Switches between basic and advanced calculator modes.
 * Updates UI elements and shows/hides appropriate panels.
 * 
 * @param {string} mode - The mode to switch to ('basic' or 'advanced')
 */
function switchMode(mode) {
    const basicBtn = document.getElementById('basicMode');
    const advancedBtn = document.getElementById('advancedMode');
    const calculator = document.getElementById('calculator');
    
    if (mode === 'basic') {
        isAdvancedMode = false;
        basicBtn.classList.add('active');
        advancedBtn.classList.remove('active');
        calculator.classList.remove('advanced-mode');
    } else {
        isAdvancedMode = true;
        advancedBtn.classList.add('active');
        basicBtn.classList.remove('active');
        calculator.classList.add('advanced-mode');
    }
}

/**
 * MEMORY FUNCTIONS
 */

/**
 * Clears the calculator memory.
 */
function memoryClear() {
    memoryValue = 0;
}

/**
 * Recalls the value stored in memory to the display.
 */
function memoryRecall() {
    currentInput = memoryValue.toString();
    shouldResetDisplay = true;
    updateDisplay();
}

/**
 * Adds the current display value to memory.
 */
function memoryAdd() {
    memoryValue += parseFloat(currentInput);
}

/**
 * Subtracts the current display value from memory.
 */
function memorySubtract() {
    memoryValue -= parseFloat(currentInput);
}

/**
 * SCIENTIFIC FUNCTIONS
 */

/**
 * Performs scientific calculations by sending requests to the server.
 * Supports trigonometric, logarithmic, and other advanced functions.
 * 
 * @param {string} func - The scientific function to apply
 */
async function scientificFunction(func) {
    const value = parseFloat(currentInput);
    
    try {
        const response = await fetch('/scientific', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                function: func, 
                value: value 
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentInput = data.result;
            shouldResetDisplay = true;
            updateDisplay();
        } else {
            showError(data.error);
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError('Network error');
    }
}

// Initialize display
updateDisplay();
