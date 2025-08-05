
# SauceDemo BDD Test Automation Suite
A comprehensive Behavior-Driven Development (BDD) test automation suite for SauceDemo using Python, Selenium, and Behave.

# 🚀 Quick Start

# Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```

git clone <repository-url>
cd saucedemo-bdd-tests

```

2.Create virtual environment
```

python -m venv venv

# Windows

venv\Scripts\activate

# macOS/Linux

source venv/bin/activate

```

3.Install dependencies
```

pip install -r requirements.txt

```

## 📁 Project Structure

```

├── features/                  \# Gherkin feature files
│   ├── login.feature         \# Login/logout scenarios
│   ├── cart.feature          \# Shopping cart functionality
│   ├── checkout.feature      \# Checkout process
│   ├── negative_scenarios.feature \# Error handling tests
│   └── steps/                \# Step definitions
│       ├── login_steps.py
│       ├── cart_steps.py
│       ├── checkout_steps.py
│       └── negative_steps.py
├── pages/                    \# Page Object Model
│   ├── base_page.py         \# Base page with common functionality
│   ├── login_page.py        \# Login page objects
│   ├── products_page.py     \# Products page objects
│   ├── cart_page.py         \# Cart page objects
│   └── checkout_page.py     \# Checkout page objects
├── utils/                   \# Utility modules
│   ├── config.py           \# Configuration management
│   └── browser_factory.py  \# WebDriver factory
├── reports/                \# Test reports and screenshots
│   ├── allure-results/     \# Allure raw results
│   └── screenshots/        \# Screenshots on failure
├── requirements.txt        \# Python dependencies
├── behave.ini             \# Behave configuration
└── README.md              \# This file

```

## 🧪 Running Tests

### Basic Execution
```


# Run all tests

behave

# Run specific feature

behave features/login.feature

# Run with specific browser

behave -D browser=chrome
behave -D browser=firefox

# Run headless

behave -D browser=chrome -D headless=true

```

### Tag-based Execution
```


# Run smoke tests only

behave --tags=@smoke

# Run positive scenarios

behave --tags=@positive

# Exclude negative tests

behave --tags=-@negative

# Run login and cart tests

behave --tags=@login,@cart

# Complex tag expressions

behave --tags=@smoke,@positive --tags=-@slow

```

### Environment Configuration
```


# Run against different environment

behave -D test_env=staging

# Run with custom configuration

behave -D browser=firefox -D headless=true -D test_env=dev

```

## 📊 Test Reporting

### Allure Reports
Generate beautiful HTML reports with Allure:

```


# Run tests and generate Allure results

behave

# Generate and serve Allure report

allure serve reports/allure-results

# Generate static HTML report

allure generate reports/allure-results -o reports/allure-report

```

### Built-in Reports
```


# Generate JUnit XML report

behave --junit --junit-directory reports/

# Generate plain text report

behave -f plain

```

## 🔧 Configuration

### Browser Setup
The test suite supports Chrome and Firefox with automatic driver management via WebDriverManager.

**Chrome** (Default)
- Automatically downloads and manages ChromeDriver
- Supports headless mode
- Optimized for CI/CD environments

**Firefox**
- Automatically downloads and manages GeckoDriver  
- Supports headless mode
- Alternative browser for cross-browser testing

### Environment Variables
```


# Set default browser

export BROWSER=chrome

# Enable headless mode

export HEADLESS=true

# Set test environment

export TEST_ENV=staging

```

## 📋 Test Scenarios

### Login Features (@login)
- ✅ Valid user login with multiple user types
- ✅ Locked user error handling
- ✅ Invalid credentials validation
- ✅ Empty field validation
- ✅ Logout functionality

### Shopping Cart (@cart)
- ✅ Add single/multiple products
- ✅ Remove products from cart
- ✅ Cart badge count verification
- ✅ Product details in cart
- ✅ Continue shopping navigation

### Checkout Process (@checkout)
- ✅ Complete checkout flow
- ✅ Checkout information validation
- ✅ Order summary verification
- ✅ Payment and shipping info display
- ✅ Missing field error handling

### Negative Scenarios (@negative)
- ✅ Direct URL access without login
- ✅ XSS attempt validation
- ✅ Browser back button behavior
- ✅ Session management

## 🎯 Test Strategy

### Testing Types
- **Functional Testing**: Core application functionality
- **UI Testing**: User interface interactions
- **Negative Testing**: Error conditions and edge cases
- **Cross-browser Testing**: Chrome and Firefox support
- **Smoke Testing**: Critical path validation

### Methodologies
- **BDD (Behavior-Driven Development)**: Gherkin scenarios
- **Page Object Model**: Maintainable page abstractions
- **Data-Driven Testing**: Scenario outlines with examples
- **Tag-based Execution**: Flexible test organization

## 🔍 Debugging and Troubleshooting

### Common Issues

**WebDriver Issues**
```


# Clear WebDriver cache

rm -rf ~/.wdm

# Reinstall dependencies

pip uninstall selenium webdriver-manager -y
pip install selenium webdriver-manager

```

**Browser Issues**
```


# Update Chrome/Firefox to latest version

# Run with different browser

behave -D browser=firefox

```

**Screenshot Analysis**
Failed test screenshots are automatically saved to `reports/screenshots/`

### Debug Mode
```


# Run with verbose output

behave -v

# Show step timings

behave --show-timings

# Capture stdout

behave --no-capture

```

## 🚀 CI/CD Integration

### GitHub Actions Example
```

name: BDD Tests
on: [push, pull_request]

jobs:
test:
runs-on: ubuntu-latest
strategy:
matrix:
browser: [chrome, firefox]

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          
      - name: Run tests
        run: |
          behave -D browser=${{ matrix.browser }} -D headless=true
          
      - name: Generate Allure Report
        run: |
          allure generate reports/allure-results -o reports/allure-report
          
      - name: Upload Allure Report
        uses: actions/upload-artifact@v3
        with:
          name: allure-report-${{ matrix.browser }}
          path: reports/allure-report
    ```

## 🐛 Bug Investigation Workflow

### Reproducing Bugs
1. **Create targeted scenario** in appropriate feature file
2. **Add specific tags** for bug tracking (e.g., @bug-123)
3. **Run isolated test**: `behave --tags=@bug-123`

### Debugging Process
1. **Enable logging**: Check `features/environment.py` 
2. **Take screenshots**: Automatically captured on failure
3. **Inspect page state**: Use browser DevTools
4. **Check WebDriver logs```

