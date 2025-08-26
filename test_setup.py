#!/usr/bin/env python3
"""
Test script to verify the email sender project setup
"""

import os
import sys
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import smtplib
        print("✓ smtplib imported successfully")
    except ImportError as e:
        print(f"✗ smtplib import failed: {e}")
        return False
    
    try:
        import email
        print("✓ email module imported successfully")
    except ImportError as e:
        print(f"✗ email module import failed: {e}")
        return False
    
    try:
        import pathlib
        print("✓ pathlib imported successfully")
    except ImportError as e:
        print(f"✗ pathlib import failed: {e}")
        return False
    
    try:
        import jinja2
        print("✓ jinja2 imported successfully")
    except ImportError as e:
        print(f"✗ jinja2 import failed: {e}")
        return False
    
    try:
        import dotenv
        print("✓ python-dotenv imported successfully")
    except ImportError as e:
        print(f"✗ python-dotenv import failed: {e}")
        return False
    
    return True

def test_files():
    """Test if all required files exist"""
    print("\nTesting required files...")
    
    required_files = [
        "template.html",
        "emails.csv",
        "email_sender.py",
        "requirements.txt"
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            all_files_exist = False
    
    return all_files_exist

def test_folders():
    """Test if all required folders exist"""
    print("\nTesting required folders...")
    
    required_folders = [
        "assets",
        "attachments",
        "venv"
    ]
    
    all_folders_exist = True
    for folder_path in required_folders:
        if Path(folder_path).exists():
            print(f"✓ {folder_path}/ exists")
        else:
            print(f"✗ {folder_path}/ missing")
            all_folders_exist = False
    
    return all_folders_exist

def test_template():
    """Test if the HTML template can be loaded and rendered"""
    print("\nTesting HTML template...")
    
    try:
        from jinja2 import Template
        
        with open("template.html", "r", encoding="utf-8") as f:
            template_content = f.read()
        
        template = Template(template_content)
        
        # Test rendering with sample data
        test_data = {
            "recipient_name": "Test User",
            "company_name": "Test Company"
        }
        
        rendered = template.render(**test_data)
        
        if "Test User" in rendered and "Test Company" in rendered:
            print("✓ Template rendered successfully with test data")
            return True
        else:
            print("✗ Template rendering failed - variables not replaced")
            return False
            
    except Exception as e:
        print(f"✗ Template test failed: {e}")
        return False

def test_csv():
    """Test if the CSV file can be read"""
    print("\nTesting CSV file...")
    
    try:
        import csv
        
        with open("emails.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        if len(rows) > 0:
            print(f"✓ CSV loaded successfully with {len(rows)} rows")
            print(f"  Columns: {list(rows[0].keys())}")
            return True
        else:
            print("✗ CSV file is empty")
            return False
            
    except Exception as e:
        print(f"✗ CSV test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Email Sender Project Setup Test")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Files", test_files),
        ("Folders", test_folders),
        ("Template", test_template),
        ("CSV", test_csv)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 40)
    print("📊 Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your email sender project is ready to use.")
        print("\nNext steps:")
        print("1. Copy env_example.txt to .env")
        print("2. Add your Gmail credentials to .env")
        print("3. Replace placeholder files in assets/ and attachments/")
        print("4. Update emails.csv with your recipient list")
        print("5. Run: python email_sender.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
