#!/usr/bin/env python3
"""
Test script for Job Board API
"""

import requests
import json

def test_api():
    base_url = "http://localhost:5002"
    
    print("🧪 Testing Job Board API...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"✅ Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test jobs endpoint
    try:
        response = requests.get(f"{base_url}/api/jobs")
        print(f"✅ Jobs endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {len(data.get('jobs', []))} jobs")
    except Exception as e:
        print(f"❌ Jobs endpoint failed: {e}")
    
    # Test registration
    try:
        user_data = {
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        }
        response = requests.post(f"{base_url}/api/auth/register", json=user_data)
        print(f"✅ Registration: {response.status_code}")
        if response.status_code == 201:
            print("   User registered successfully")
    except Exception as e:
        print(f"❌ Registration failed: {e}")
    
    # Test login
    try:
        login_data = {
            "email": "admin@jobboard.com",
            "password": "admin123"
        }
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        print(f"✅ Login: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Login successful for: {data.get('user', {}).get('name')}")
            return data.get('access_token')
    except Exception as e:
        print(f"❌ Login failed: {e}")
    
    return None

def test_authenticated_endpoints(token):
    if not token:
        print("❌ No token available for authenticated tests")
        return
    
    base_url = "http://localhost:5002"
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🔐 Testing authenticated endpoints...")
    
    # Test user profile
    try:
        response = requests.get(f"{base_url}/api/users/profile", headers=headers)
        print(f"✅ User profile: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   User: {data.get('name')} ({data.get('email')})")
    except Exception as e:
        print(f"❌ User profile failed: {e}")
    
    # Test job application
    try:
        app_data = {"job_id": 1}
        response = requests.post(f"{base_url}/api/applications", json=app_data, headers=headers)
        print(f"✅ Job application: {response.status_code}")
        if response.status_code == 201:
            print("   Application submitted successfully")
    except Exception as e:
        print(f"❌ Job application failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting Job Board API Tests...")
    token = test_api()
    test_authenticated_endpoints(token)
    print("\n✨ Testing complete!") 