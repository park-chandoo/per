# Flask Web Application - Bug Fixes Demo

This repository demonstrates the identification and fixing of critical bugs in a Flask web application. The application was intentionally created with several security vulnerabilities and performance issues, which have been systematically identified and resolved.

## Overview

The application is a simple user management system with the following features:
- User registration and login
- User search functionality
- User profile retrieval

## Critical Bugs Fixed

### 1. SQL Injection Vulnerability (Security Critical)
- **Problem**: Direct string concatenation in SQL queries
- **Fix**: Parameterized queries with proper input sanitization
- **Impact**: Prevents database compromise and data theft

### 2. Weak Password Hashing (Security Critical)
- **Problem**: Using MD5 for password hashing
- **Fix**: bcrypt with salt for secure password storage
- **Impact**: Protects user passwords from rainbow table attacks

### 3. Inefficient Search Algorithm (Performance Issue)
- **Problem**: Loading all data into memory for filtering
- **Fix**: Database-level filtering with LIKE operator
- **Impact**: Improved performance and reduced memory usage

## Files

- `app.py` - Main Flask application with all fixes applied
- `init_db.py` - Database initialization script
- `requirements.txt` - Python dependencies
- `test_fixes.py` - Test script to verify bug fixes
- `BUG_FIXES.md` - Detailed documentation of all bugs and fixes

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Initialize the database:
   ```bash
   python3 init_db.py
   ```

3. Run the application:
   ```bash
   python3 app.py
   ```

4. Test the fixes:
   ```bash
   python3 test_fixes.py
   ```

## Security Improvements

- ✅ SQL injection prevention
- ✅ Secure password hashing
- ✅ Environment-based configuration
- ✅ Production-safe settings
- ✅ Input validation

## Performance Improvements

- ✅ Optimized database queries
- ✅ Reduced memory usage
- ✅ Better scalability

## Testing

The `test_fixes.py` script verifies that all critical bugs have been properly fixed and the application functions correctly.
