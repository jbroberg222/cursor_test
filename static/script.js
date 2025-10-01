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
 * Shows a dialog with version information and credits.
 * Displays a modal dialog with attribution message.
 */
function showVersionDialog() {
    // Create modal overlay
    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);
    `;
    
    // Create dialog box
    const dialog = document.createElement('div');
    dialog.style.cssText = `
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        max-width: 400px;
        margin: 20px;
        color: white;
        font-family: 'Inter', sans-serif;
    `;
    
    // Create dialog content
    dialog.innerHTML = `
        <h3 style="margin: 0 0 16px 0; font-size: 18px; font-weight: 600;">Calculator v 0.18</h3>
        <p style="margin: 0 0 24px 0; font-size: 14px; line-height: 1.5; opacity: 0.9;">
            Brought to you by Jeff Broberg and his buddy cursor.ai
        </p>
        <button id="closeDialog" style="
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 8px 16px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s ease;
        ">Close</button>
    `;
    
    // Add dialog to overlay
    overlay.appendChild(dialog);
    
    // Add overlay to body
    document.body.appendChild(overlay);
    
    // Add close functionality
    const closeBtn = dialog.querySelector('#closeDialog');
    const closeDialog = () => {
        document.body.removeChild(overlay);
    };
    
    closeBtn.addEventListener('click', closeDialog);
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            closeDialog();
        }
    });
    
    // Add hover effect to close button
    closeBtn.addEventListener('mouseenter', () => {
        closeBtn.style.background = 'rgba(255, 255, 255, 0.3)';
    });
    closeBtn.addEventListener('mouseleave', () => {
        closeBtn.style.background = 'rgba(255, 255, 255, 0.2)';
    });
}

/**
 * Updates the calculator display with the current input value.
 */
function updateDisplay() {
    console.log(`[DEBUG] updateDisplay() called - Setting display to: "${currentInput}"`);
    display.textContent = currentInput;
    console.log(`[DEBUG] updateDisplay() completed - Display now shows: "${display.textContent}"`);
}

/**
 * Clears all calculator state and resets to initial state.
 * Clears current input, operator, previous input, and resets display flag.
 */
function clearAll() {
    console.log(`[DEBUG] clearAll() called - Previous state: currentInput="${currentInput}", operator="${operator}", previousInput="${previousInput}", shouldResetDisplay=${shouldResetDisplay}`);
    currentInput = '0';
    operator = null;
    previousInput = null;
    shouldResetDisplay = false;
    console.log(`[DEBUG] clearAll() completed - New state: currentInput="${currentInput}", operator="${operator}", previousInput="${previousInput}", shouldResetDisplay=${shouldResetDisplay}`);
    updateDisplay();
}

/**
 * Clears only the current entry, leaving operator and previous input intact.
 */
function clearEntry() {
    console.log(`[DEBUG] clearEntry() called - Previous currentInput: "${currentInput}", operator: "${operator}", previousInput: "${previousInput}"`);
    currentInput = '0';
    console.log(`[DEBUG] clearEntry() completed - New currentInput: "${currentInput}"`);
    updateDisplay();
}

/**
 * Removes the last character from the current input.
 * If only one character remains, resets to '0'.
 */
function backspace() {
    console.log(`[DEBUG] backspace() called - Previous currentInput: "${currentInput}" (length: ${currentInput.length})`);
    if (currentInput.length > 1) {
        currentInput = currentInput.slice(0, -1);
        console.log(`[DEBUG] backspace() - Removed last character, new currentInput: "${currentInput}"`);
    } else {
        currentInput = '0';
        console.log(`[DEBUG] backspace() - Reset to '0' (was single character)`);
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
    console.log(`[DEBUG] appendToDisplay('${value}') called - Current state: currentInput="${currentInput}", shouldResetDisplay=${shouldResetDisplay}`);
    
    if (shouldResetDisplay) {
        console.log(`[DEBUG] appendToDisplay() - Resetting display (shouldResetDisplay was true)`);
        currentInput = '0';
        shouldResetDisplay = false;
    }
    
    if (value === '.' && currentInput.includes('.')) {
        console.log(`[DEBUG] appendToDisplay() - Ignoring decimal point (already exists)`);
        return; // Prevent multiple decimal points
    }
    
    if (currentInput === '0' && value !== '.') {
        console.log(`[DEBUG] appendToDisplay() - Replacing '0' with '${value}'`);
        currentInput = value;
    } else {
        console.log(`[DEBUG] appendToDisplay() - Appending '${value}' to '${currentInput}'`);
        currentInput += value;
    }
    
    console.log(`[DEBUG] appendToDisplay() completed - New currentInput: "${currentInput}"`);
    updateDisplay();
}

/**
 * Sets the operator for the next calculation.
 * If an operator is already set, performs the calculation first.
 * 
 * @param {string} op - The operator symbol (+, -, ×, ÷)
 */
function setOperator(op) {
    console.log(`[DEBUG] setOperator('${op}') called - Current state: operator="${operator}", previousInput="${previousInput}", currentInput="${currentInput}"`);
    
    if (operator && previousInput !== null) {
        console.log(`[DEBUG] setOperator() - Performing calculation before setting new operator`);
        calculate();
    }
    
    operator = op;
    previousInput = currentInput;
    shouldResetDisplay = true;
    console.log(`[DEBUG] setOperator() completed - New state: operator="${operator}", previousInput="${previousInput}", shouldResetDisplay=${shouldResetDisplay}`);
}

/**
 * Performs the calculation using the stored operator and operands.
 * Handles basic arithmetic operations with proper error checking.
 */
function calculate() {
    console.log(`[DEBUG] calculate() called - State: operator="${operator}", previousInput="${previousInput}", currentInput="${currentInput}"`);
    
    if (operator && previousInput !== null) {
        const prev = parseFloat(previousInput);
        const current = parseFloat(currentInput);
        console.log(`[DEBUG] calculate() - Parsed values: prev=${prev}, current=${current}`);
        
        let result;
        
        switch (operator) {
            case '+':
                result = prev + current;
                console.log(`[DEBUG] calculate() - Addition: ${prev} + ${current} = ${result}`);
                break;
            case '-':
                result = prev - current;
                console.log(`[DEBUG] calculate() - Subtraction: ${prev} - ${current} = ${result}`);
                break;
            case '×':
                result = prev * current;
                console.log(`[DEBUG] calculate() - Multiplication: ${prev} × ${current} = ${result}`);
                break;
            case '÷':
                if (current === 0) {
                    console.log(`[DEBUG] calculate() - Division by zero error`);
                    showError('Division by zero');
                    return;
                }
                result = prev / current;
                console.log(`[DEBUG] calculate() - Division: ${prev} ÷ ${current} = ${result}`);
                break;
            default:
                console.log(`[DEBUG] calculate() - Unknown operator: ${operator}`);
                return;
        }
        
        // Round to avoid floating point precision issues
        result = Math.round(result * 10000000000) / 10000000000;
        console.log(`[DEBUG] calculate() - Rounded result: ${result}`);
        
        currentInput = result.toString();
        operator = null;
        previousInput = null;
        shouldResetDisplay = true;
        console.log(`[DEBUG] calculate() completed - New state: currentInput="${currentInput}", operator="${operator}", previousInput="${previousInput}"`);
        updateDisplay();
    } else {
        console.log(`[DEBUG] calculate() - No calculation performed (missing operator or previousInput)`);
    }
}

/**
 * Enhanced calculate function that sends calculations to the server.
 * Provides server-side calculation with loading states and error handling.
 */
async function calculateServer() {
    console.log(`[DEBUG] calculateServer() called - State: currentInput="${currentInput}", operator="${operator}", previousInput="${previousInput}"`);
    
    // Don't calculate if there's no meaningful input
    if (currentInput === '0' && !operator && !previousInput) {
        console.log(`[DEBUG] calculateServer() - No calculation needed (no meaningful input)`);
        return;
    }
    
    try {
        // Show loading state
        const equalsBtn = document.querySelector('.btn-equals');
        equalsBtn.classList.add('loading');
        console.log(`[DEBUG] calculateServer() - Added loading state to equals button`);
        
        // Build the complete expression
        let expression = currentInput;
        if (operator && previousInput !== null) {
            expression = previousInput + operator + currentInput;
        }
        console.log(`[DEBUG] calculateServer() - Built expression: "${expression}"`);
        
        console.log(`[DEBUG] calculateServer() - Sending POST request to /calculate`);
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ expression: expression })
        });
        
        console.log(`[DEBUG] calculateServer() - Received response: status=${response.status}`);
        const data = await response.json();
        console.log(`[DEBUG] calculateServer() - Response data:`, data);
        
        if (response.ok) {
            console.log(`[DEBUG] calculateServer() - Success! Result: "${data.result}"`);
            currentInput = data.result;
            operator = null;
            previousInput = null;
            shouldResetDisplay = true;
            updateDisplay();
        } else {
            console.log(`[DEBUG] calculateServer() - Error: ${data.error}`);
            showError(data.error);
        }
        
    } catch (error) {
        console.error(`[DEBUG] calculateServer() - Network error:`, error);
        showError('Network error');
    } finally {
        // Remove loading state
        const equalsBtn = document.querySelector('.btn-equals');
        equalsBtn.classList.remove('loading');
        console.log(`[DEBUG] calculateServer() - Removed loading state`);
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

// Keyboard shortcuts removed - buttons only

// Event delegation for all calculator buttons
document.addEventListener('DOMContentLoaded', function() {
    console.log(`[DEBUG] DOMContentLoaded event - Initializing calculator with event delegation`);
    
    // Initialize the live timestamp
    console.log(`[DEBUG] DOMContentLoaded - Initializing timestamp`);
    initializeTimestamp();
    
    // Add click handler for version number
    const versionElement = document.getElementById('version');
    console.log(`[DEBUG] DOMContentLoaded - Found version element: ${!!versionElement}`);
    if (versionElement) {
        versionElement.addEventListener('click', showVersionDialog);
        versionElement.style.cursor = 'pointer';
        console.log(`[DEBUG] DOMContentLoaded - Added version dialog click handler`);
    }
    
    // Event delegation for all calculator buttons
    document.addEventListener('click', function(event) {
        const button = event.target.closest('button');
        if (!button) return;
        
        const action = button.dataset.action;
        console.log(`[DEBUG] Button clicked - Action: "${action}", Button: "${button.textContent}"`);
        
        switch (action) {
            case 'number':
                const value = button.dataset.value;
                console.log(`[DEBUG] Number button clicked - Value: "${value}"`);
                appendToDisplay(value);
                break;
                
            case 'operator':
                const operator = button.dataset.operator;
                console.log(`[DEBUG] Operator button clicked - Operator: "${operator}"`);
                setOperator(operator);
                break;
                
            case 'calculate':
                console.log(`[DEBUG] Calculate button clicked`);
                calculateServer();
                break;
                
            case 'clear-all':
                console.log(`[DEBUG] Clear All button clicked`);
                clearAll();
                break;
                
            case 'clear-entry':
                console.log(`[DEBUG] Clear Entry button clicked`);
                clearEntry();
                break;
                
            case 'backspace':
                console.log(`[DEBUG] Backspace button clicked`);
                backspace();
                break;
                
            case 'memory-clear':
                console.log(`[DEBUG] Memory Clear button clicked`);
                memoryClear();
                break;
                
            case 'memory-recall':
                console.log(`[DEBUG] Memory Recall button clicked`);
                memoryRecall();
                break;
                
            case 'memory-add':
                console.log(`[DEBUG] Memory Add button clicked`);
                memoryAdd();
                break;
                
            case 'memory-subtract':
                console.log(`[DEBUG] Memory Subtract button clicked`);
                memorySubtract();
                break;
                
            case 'scientific':
                const functionName = button.dataset.function;
                console.log(`[DEBUG] Scientific function button clicked - Function: "${functionName}"`);
                scientificFunction(functionName);
                break;
                
            default:
                console.log(`[DEBUG] Unknown button action: "${action}"`);
                break;
        }
    });
    
    // Event delegation for mode toggle buttons
    document.addEventListener('click', function(event) {
        const button = event.target.closest('.mode-btn');
        if (!button) return;
        
        const mode = button.dataset.mode;
        console.log(`[DEBUG] Mode toggle button clicked - Mode: "${mode}"`);
        switchMode(mode);
    });
    
    console.log(`[DEBUG] DOMContentLoaded - Event delegation setup complete`);
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
    console.log(`[DEBUG] switchMode('${mode}') called - Current isAdvancedMode: ${isAdvancedMode}`);
    
    const basicBtn = document.getElementById('basicMode');
    const advancedBtn = document.getElementById('advancedMode');
    const calculator = document.getElementById('calculator');
    
    console.log(`[DEBUG] switchMode() - Found elements: basicBtn=${!!basicBtn}, advancedBtn=${!!advancedBtn}, calculator=${!!calculator}`);
    
    if (mode === 'basic') {
        console.log(`[DEBUG] switchMode() - Switching to basic mode`);
        isAdvancedMode = false;
        basicBtn.classList.add('active');
        advancedBtn.classList.remove('active');
        calculator.classList.remove('advanced-mode');
        console.log(`[DEBUG] switchMode() - Basic mode activated - isAdvancedMode: ${isAdvancedMode}`);
    } else {
        console.log(`[DEBUG] switchMode() - Switching to advanced mode`);
        isAdvancedMode = true;
        advancedBtn.classList.add('active');
        basicBtn.classList.remove('active');
        calculator.classList.add('advanced-mode');
        console.log(`[DEBUG] switchMode() - Advanced mode activated - isAdvancedMode: ${isAdvancedMode}`);
    }
}

/**
 * MEMORY FUNCTIONS
 */

/**
 * Clears the calculator memory.
 */
function memoryClear() {
    console.log(`[DEBUG] memoryClear() called - Previous memoryValue: ${memoryValue}`);
    memoryValue = 0;
    console.log(`[DEBUG] memoryClear() completed - New memoryValue: ${memoryValue}`);
}

/**
 * Recalls the value stored in memory to the display.
 */
function memoryRecall() {
    console.log(`[DEBUG] memoryRecall() called - memoryValue: ${memoryValue}, currentInput: "${currentInput}"`);
    currentInput = memoryValue.toString();
    shouldResetDisplay = true;
    console.log(`[DEBUG] memoryRecall() completed - New currentInput: "${currentInput}"`);
    updateDisplay();
}

/**
 * Adds the current display value to memory.
 */
function memoryAdd() {
    const valueToAdd = parseFloat(currentInput);
    console.log(`[DEBUG] memoryAdd() called - Adding ${valueToAdd} to memory. Previous memoryValue: ${memoryValue}`);
    memoryValue += valueToAdd;
    console.log(`[DEBUG] memoryAdd() completed - New memoryValue: ${memoryValue}`);
}

/**
 * Subtracts the current display value from memory.
 */
function memorySubtract() {
    const valueToSubtract = parseFloat(currentInput);
    console.log(`[DEBUG] memorySubtract() called - Subtracting ${valueToSubtract} from memory. Previous memoryValue: ${memoryValue}`);
    memoryValue -= valueToSubtract;
    console.log(`[DEBUG] memorySubtract() completed - New memoryValue: ${memoryValue}`);
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
    console.log(`[DEBUG] scientificFunction('${func}') called - Input value: ${value} (parsed from "${currentInput}")`);
    
    try {
        console.log(`[DEBUG] scientificFunction() - Sending POST request to /scientific with function="${func}", value=${value}`);
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
        
        console.log(`[DEBUG] scientificFunction() - Received response: status=${response.status}`);
        const data = await response.json();
        console.log(`[DEBUG] scientificFunction() - Response data:`, data);
        
        if (response.ok) {
            console.log(`[DEBUG] scientificFunction() - Success! Result: "${data.result}"`);
            currentInput = data.result;
            shouldResetDisplay = true;
            updateDisplay();
        } else {
            console.log(`[DEBUG] scientificFunction() - Error: ${data.error}`);
            showError(data.error);
        }
        
    } catch (error) {
        console.error(`[DEBUG] scientificFunction() - Network error:`, error);
        showError('Network error');
    }
}

// Initialize display
console.log(`[DEBUG] Script loaded - Initializing display`);
updateDisplay();
console.log(`[DEBUG] Calculator script fully loaded and ready`);
