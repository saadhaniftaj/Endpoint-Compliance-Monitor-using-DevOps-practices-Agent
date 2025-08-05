#!/usr/bin/env python3
"""
Comprehensive test script for the CarbonCompliance Download Application
"""

import requests
import json
import sys
from datetime import datetime

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8080/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_download_apis():
    """Test all download API endpoints"""
    print("\n🔍 Testing download APIs...")
    platforms = ["macos", "linux", "windows"]
    all_passed = True
    
    for platform in platforms:
        try:
            response = requests.get(f"http://localhost:8080/api/download/{platform}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {platform.upper()} API: {data['binary_name']}")
            else:
                print(f"❌ {platform.upper()} API failed: {response.status_code}")
                all_passed = False
        except Exception as e:
            print(f"❌ {platform.upper()} API error: {e}")
            all_passed = False
    
    return all_passed

def test_error_handling():
    """Test error handling for invalid requests"""
    print("\n🔍 Testing error handling...")
    try:
        response = requests.get("http://localhost:8080/api/download/invalid")
        if response.status_code == 400:
            data = response.json()
            print(f"✅ Error handling works: {data['detail']}")
            return True
        else:
            print(f"❌ Error handling failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error handling test error: {e}")
        return False

def test_main_page():
    """Test the main download page"""
    print("\n🔍 Testing main page...")
    try:
        response = requests.get("http://localhost:8080/")
        if response.status_code == 200:
            content = response.text
            if "CarbonCompliance" in content and "Download Agent" in content:
                print("✅ Main page loads correctly")
                return True
            else:
                print("❌ Main page content missing")
                return False
        else:
            print(f"❌ Main page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Main page error: {e}")
        return False

def test_static_files():
    """Test static file serving"""
    print("\n🔍 Testing static files...")
    try:
        response = requests.get("http://localhost:8080/static/carbonteq_logo.jpeg")
        if response.status_code == 200:
            print("✅ Logo file accessible")
            return True
        else:
            print(f"❌ Logo file failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Static files error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting CarbonCompliance Download App Tests")
    print("=" * 50)
    print(f"Timestamp: {datetime.now()}")
    print(f"Target: http://localhost:8080")
    print("=" * 50)
    
    tests = [
        ("Health Endpoint", test_health_endpoint),
        ("Download APIs", test_download_apis),
        ("Error Handling", test_error_handling),
        ("Main Page", test_main_page),
        ("Static Files", test_static_files),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The download application is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the application.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 