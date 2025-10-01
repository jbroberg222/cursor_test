# Pre-commit Hooks Documentation

This project includes pre-commit hooks to ensure code quality by running unit tests before each commit.

## 🧪 **What It Does**

The pre-commit hook automatically:
- ✅ Runs all unit tests before allowing a commit
- ❌ Blocks commits if more than 10% of tests fail
- 📊 Shows detailed test results and failure rates
- 🔧 Provides helpful error messages and fix suggestions

## 🚀 **Quick Start**

### **Enable Basic Hook (Recommended):**
```bash
./setup-pre-commit.sh basic
```

### **Enable Advanced Hook (with coverage):**
```bash
./setup-pre-commit.sh advanced
```

### **Disable Hook:**
```bash
./setup-pre-commit.sh disable
```

### **Check Status:**
```bash
./setup-pre-commit.sh status
```

## 📋 **Hook Types**

### **Basic Hook (`pre-commit`)**
- Runs unit tests with `pytest`
- Blocks commit if >10% of tests fail
- Fast execution
- **Threshold**: 10% failure rate

### **Advanced Hook (`pre-commit-advanced`)**
- Runs unit tests with coverage analysis
- Blocks commit if >10% of tests fail
- Warns if coverage drops below 80%
- **Thresholds**: 10% failure rate, 80% coverage

## 🎯 **How It Works**

### **When You Commit:**
```bash
git commit -m "Your commit message"
```

### **What Happens:**
1. 🧪 Pre-commit hook runs automatically
2. 📊 Tests execute and results are analyzed
3. ✅ **If tests pass**: Commit proceeds normally
4. ❌ **If tests fail**: Commit is blocked with helpful message

### **Example Output (Success):**
```
🧪 Running unit tests before commit...
==================================
Running pytest...
📊 Test Results:
   Total Tests: 26
   Passed: 26
   Failed: 0
   Failure Rate: 0%
==================================
✅ COMMIT ALLOWED: Failure rate (0%) is within acceptable range
==================================
```

### **Example Output (Blocked):**
```
🧪 Running unit tests before commit...
==================================
Running pytest...
📊 Test Results:
   Total Tests: 26
   Passed: 21
   Failed: 5
   Failure Rate: 19%
==================================
❌ COMMIT BLOCKED: Failure rate (19%) exceeds 10% threshold

🔧 To fix this:
   1. Fix failing tests
   2. Run: python3 -m pytest test_app.py -v
   3. Try committing again

💡 To bypass this check (not recommended):
   git commit --no-verify
==================================
```

## ⚙️ **Configuration**

### **Adjust Thresholds:**
Edit `.git/hooks/pre-commit-config`:
```bash
# Maximum allowed test failure rate (percentage)
MAX_FAILURE_RATE=10

# Minimum required test coverage (percentage)
MIN_COVERAGE=80
```

### **Custom Test Command:**
Modify the hook files to change which tests run or how they're executed.

## 🛠️ **Troubleshooting**

### **Hook Not Running:**
```bash
# Check if hook is executable
ls -la .git/hooks/pre-commit

# Re-enable hook
./setup-pre-commit.sh basic
```

### **Tests Failing:**
```bash
# Run tests manually to see details
python3 -m pytest test_app.py -v

# Fix failing tests, then try committing again
```

### **Bypass Hook (Not Recommended):**
```bash
# Skip pre-commit hook for this commit only
git commit --no-verify -m "Emergency fix"
```

## 📊 **Current Test Status**

- **Total Tests**: 26
- **Currently Passing**: 21
- **Currently Failing**: 5
- **Failure Rate**: 19% (exceeds 10% threshold)
- **Coverage**: 85%

## 🎯 **Benefits**

- 🛡️ **Prevents Broken Code**: No commits with failing tests
- 📈 **Maintains Quality**: Ensures test suite stays healthy
- 🔄 **Automated**: No manual test running required
- 📊 **Visibility**: Clear feedback on test status
- 🚀 **Team Consistency**: Same standards for all developers

## 💡 **Best Practices**

1. **Fix Tests First**: Don't bypass the hook - fix failing tests
2. **Run Tests Locally**: `python3 -m pytest test_app.py -v` before committing
3. **Keep Thresholds Reasonable**: 10% failure rate allows for some test maintenance
4. **Use Advanced Hook**: For projects requiring high coverage
5. **Team Alignment**: Ensure all team members use the same hook settings

## 🔧 **Advanced Usage**

### **Custom Hook Script:**
Create your own hook by copying and modifying the existing ones:
```bash
cp .git/hooks/pre-commit .git/hooks/pre-commit-custom
# Edit the custom hook
chmod +x .git/hooks/pre-commit-custom
```

### **Multiple Hooks:**
Git supports multiple pre-commit hooks. Add additional checks by creating more hook files.

### **CI Integration:**
The same test commands can be used in CI/CD pipelines for consistency.
