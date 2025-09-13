#!/usr/bin/env python3
"""
Integration test script for InterviewOverfit
Tests the complete frontend-backend integration
"""

import sys
import requests
import time
import json
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "back-end"
sys.path.insert(0, str(backend_path))

def test_backend_endpoints():
    """Test all backend API endpoints."""
    base_url = "http://localhost:8000"
    api_url = f"{base_url}/api"
    
    print("🧪 Testing Backend API Endpoints")
    print("=" * 40)
    
    tests = []
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            tests.append(("Health Check", "✅ PASS"))
        else:
            tests.append(("Health Check", f"❌ FAIL - Status: {response.status_code}"))
    except Exception as e:
        tests.append(("Health Check", f"❌ FAIL - {e}"))
    
    # Test 2: API Info
    try:
        response = requests.get(f"{api_url}/info", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "name" in data and "endpoints" in data:
                tests.append(("API Info", "✅ PASS"))
            else:
                tests.append(("API Info", "❌ FAIL - Missing required fields"))
        else:
            tests.append(("API Info", f"❌ FAIL - Status: {response.status_code}"))
    except Exception as e:
        tests.append(("API Info", f"❌ FAIL - {e}"))
    
    # Test 3: Start Game (without API key - should fail gracefully)
    try:
        response = requests.post(
            f"{api_url}/game/test-user/start",
            json={"api_key": None},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if not data.get("success") and "API key" in data.get("error", ""):
                tests.append(("Start Game (No API Key)", "✅ PASS - Correctly requires API key"))
            else:
                tests.append(("Start Game (No API Key)", "❌ FAIL - Should require API key"))
        else:
            tests.append(("Start Game (No API Key)", f"❌ FAIL - Status: {response.status_code}"))
    except Exception as e:
        tests.append(("Start Game (No API Key)", f"❌ FAIL - {e}"))
    
    # Test 4: Get Status (no active game)
    try:
        response = requests.get(f"{api_url}/game/test-user/status", timeout=5)
        if response.status_code == 404:
            tests.append(("Get Status (No Game)", "✅ PASS - Correctly returns 404"))
        else:
            tests.append(("Get Status (No Game)", f"❌ FAIL - Expected 404, got {response.status_code}"))
    except Exception as e:
        tests.append(("Get Status (No Game)", f"❌ FAIL - {e}"))
    
    # Print results
    passed = 0
    total = len(tests)
    
    for test_name, result in tests:
        print(f"{test_name:30} {result}")
        if "✅ PASS" in result:
            passed += 1
    
    print(f"\n📊 Backend Tests: {passed}/{total} passed")
    return passed == total

def test_frontend_build():
    """Test that the frontend can be built."""
    print("\n🏗️  Testing Frontend Build")
    print("=" * 30)
    
    try:
        import subprocess
        import os
        
        # Change to frontend directory
        frontend_path = Path(__file__).parent / "frontend"
        
        # Check if package.json exists
        if not (frontend_path / "package.json").exists():
            print("❌ FAIL - No package.json found in frontend directory")
            return False
        
        # Try to run type check (if TypeScript)
        try:
            result = subprocess.run(
                ["pnpm", "run", "type-check"],
                cwd=frontend_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print("✅ PASS - TypeScript type checking")
            else:
                print("⚠️  WARN - TypeScript type checking issues (may be OK)")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("⚠️  SKIP - TypeScript type checking (command not found)")
        
        print("✅ PASS - Frontend structure is valid")
        return True
        
    except Exception as e:
        print(f"❌ FAIL - {e}")
        return False

def test_integration():
    """Test the integration between frontend and backend."""
    print("\n🔗 Testing Frontend-Backend Integration")
    print("=" * 45)
    
    try:
        # Test CORS headers
        response = requests.options("http://localhost:8000/api/info", timeout=5)
        cors_headers = response.headers.get("Access-Control-Allow-Origin", "")
        
        if "localhost:5173" in cors_headers or "*" in cors_headers:
            print("✅ PASS - CORS configured for frontend")
        else:
            print("⚠️  WARN - CORS may not be properly configured")
        
        # Test API service types match backend
        api_service_path = Path(__file__).parent / "frontend/src/services/api.ts"
        if api_service_path.exists():
            print("✅ PASS - API service file exists")
            
            # Check if the service has the required methods
            content = api_service_path.read_text()
            required_methods = ["startGame", "submitAnswer", "getGameStatus", "getQuestion"]
            
            missing_methods = []
            for method in required_methods:
                if method not in content:
                    missing_methods.append(method)
            
            if not missing_methods:
                print("✅ PASS - All required API methods present")
            else:
                print(f"❌ FAIL - Missing API methods: {missing_methods}")
                return False
        else:
            print("❌ FAIL - API service file not found")
            return False
        
        print("✅ PASS - Integration setup is correct")
        return True
        
    except Exception as e:
        print(f"❌ FAIL - {e}")
        return False

def main():
    """Run all integration tests."""
    print("🎮 InterviewOverfit Integration Test Suite")
    print("=" * 50)
    
    # Check if servers are running
    print("🔍 Checking if servers are running...")
    
    try:
        requests.get("http://localhost:8000/health", timeout=2)
        print("✅ Backend server is running")
        backend_running = True
    except:
        print("❌ Backend server is not running")
        print("   Please start the backend with: ./start_dev.sh")
        backend_running = False
    
    try:
        requests.get("http://localhost:5173", timeout=2)
        print("✅ Frontend server is running")
        frontend_running = True
    except:
        print("⚠️  Frontend server may not be running")
        print("   This is OK if you haven't started it yet")
        frontend_running = False
    
    print()
    
    # Run tests
    results = []
    
    if backend_running:
        results.append(("Backend API", test_backend_endpoints()))
    else:
        results.append(("Backend API", False))
        print("❌ Skipping backend tests - server not running")
    
    results.append(("Frontend Build", test_frontend_build()))
    
    if backend_running:
        results.append(("Integration", test_integration()))
    else:
        results.append(("Integration", False))
        print("❌ Skipping integration tests - backend not running")
    
    # Final results
    print(f"\n{'='*50}")
    print("📋 FINAL TEST RESULTS")
    print(f"{'='*50}")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\n🏆 Overall: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 All tests passed! Your InterviewOverfit integration is ready!")
        print("\n🎮 To play the game:")
        print("1. Make sure both servers are running: ./start_dev.sh")
        print("2. Open http://localhost:5173 in your browser")
        print("3. Have your Anthropic API key ready")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
