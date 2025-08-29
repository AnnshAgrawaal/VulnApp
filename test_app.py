#!/usr/bin/env python3
'''
Simple test script to validate VulnApp functionality
Run this script to check if the application starts correctly
'''

import subprocess
import time
import requests
import threading
import sys

def start_server():
    '''Start the Flask server in a subprocess'''
    return subprocess.Popen([
        sys.executable, 'app.py'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def test_endpoints():
    '''Test basic endpoints to ensure they respond'''
    base_url = 'http://localhost:5000'

    endpoints = [
        '/',
        '/login',
        '/register', 
        '/dashboard',
        '/admin',
        '/settings'
    ]

    print("Testing endpoints...")

    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            status = "✅" if response.status_code == 200 else "❌"
            print(f"{status} {endpoint} - Status: {response.status_code}")
        except requests.RequestException as e:
            print(f"❌ {endpoint} - Error: {e}")

def test_sql_injection():
    '''Test SQL injection vulnerability'''
    print("\nTesting SQL injection...")

    payload = {
        'username': "' OR '1'='1' --",
        'password': "anything"
    }

    try:
        response = requests.post('http://localhost:5000/login', data=payload, timeout=5)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ SQL injection test successful - Vulnerability confirmed!")
            else:
                print("❌ SQL injection test failed")
        else:
            print(f"❌ Login endpoint error: {response.status_code}")
    except Exception as e:
        print(f"❌ SQL injection test error: {e}")

def main():
    print("VulnApp Test Script")
    print("=" * 50)

    # Start server
    print("Starting Flask server...")
    server_process = start_server()

    # Wait for server to start
    time.sleep(3)

    try:
        # Test endpoints
        test_endpoints()

        # Test vulnerability
        test_sql_injection()

        print("\n" + "=" * 50)
        print("Test completed! Server is running at http://localhost:5000")
        print("Press Ctrl+C to stop the server")

        # Keep server running
        server_process.wait()

    except KeyboardInterrupt:
        print("\nShutting down server...")
        server_process.terminate()
        server_process.wait()

if __name__ == '__main__':
    main()
