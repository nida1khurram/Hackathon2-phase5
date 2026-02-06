#!/usr/bin/env python3
"""
Simple script to test backend connectivity and basic functionality
"""
import requests
import json

API_BASE = "http://localhost:8000"

def test_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print("✅ Backend is running!")
            return True
        else:
            print("❌ Backend health check failed")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running on port 8000?")
        return False

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("\n--- Testing Authentication ---")
    
    # Test registration
    test_user = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        # Try to register
        response = requests.post(f"{API_BASE}/auth/register", json=test_user)
        print(f"Registration: {response.status_code}")
        
        if response.status_code == 400:
            print("User might already exist, trying login...")
        elif response.status_code == 200:
            print("✅ Registration successful")
        
        # Try to login
        response = requests.post(f"{API_BASE}/auth/login", json=test_user)
        print(f"Login: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print("✅ Login successful")
            print(f"Token (first 20 chars): {token[:20]}...")
            return token
        else:
            print("❌ Login failed")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Auth test failed: {e}")
        return None

def test_tasks_endpoints(token):
    """Test task endpoints with authentication"""
    if not token:
        print("❌ No token available for task testing")
        return
        
    print("\n--- Testing Tasks ---")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Get tasks
        response = requests.get(f"{API_BASE}/tasks", headers=headers)
        print(f"Get tasks: {response.status_code}")
        
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Found {len(tasks)} tasks")
            
            # Create a test task
            test_task = {
                "title": "Test Task",
                "description": "This is a test task",
                "completed": False
            }
            
            response = requests.post(f"{API_BASE}/tasks", json=test_task, headers=headers)
            print(f"Create task: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Task creation successful")
                created_task = response.json()
                task_id = created_task["id"]
                
                # Update the task
                update_data = {"completed": True}
                response = requests.put(f"{API_BASE}/tasks/{task_id}", json=update_data, headers=headers)
                print(f"Update task: {response.status_code}")
                
                if response.status_code == 200:
                    print("✅ Task update successful")
                
                # Delete the task
                response = requests.delete(f"{API_BASE}/tasks/{task_id}", headers=headers)
                print(f"Delete task: {response.status_code}")
                
                if response.status_code == 200:
                    print("✅ Task deletion successful")
            else:
                print("❌ Task creation failed")
                print(f"Response: {response.text}")
        else:
            print("❌ Get tasks failed")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Tasks test failed: {e}")

def main():
    print("🔍 Testing Backend Connectivity...")
    
    if not test_health():
        print("\n❌ Backend is not running. Please start it with:")
        print("cd backend && python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    token = test_auth_endpoints()
    test_tasks_endpoints(token)
    
    print("\n🎉 Backend testing complete!")

if __name__ == "__main__":
    main()