#!/usr/bin/env python3
"""
Simple script to start a local Qdrant instance for development
"""
import subprocess
import sys
import time
import requests
from pathlib import Path

def check_qdrant_running():
    """Check if Qdrant is already running on port 6333"""
    try:
        response = requests.get("http://localhost:6333/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def main():
    print("🔍 Checking if Qdrant is already running...")

    if check_qdrant_running():
        print("✅ Qdrant is already running on http://localhost:6333")
        return True

    print("❌ Qdrant is not running. Please make sure Docker Desktop is running and execute:")
    print("   docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant")
    print("\nOr install Qdrant using: pip install qdrant-server")
    print("Then run: qdrant-server")

    # Try to install and run qdrant-server if available
    try:
        import qdrant_server
        print("✅ Found qdrant-server package, but it may need to be run separately")
    except ImportError:
        print("💡 Qdrant server not available as a Python package in this environment")
        print("💡 The recommended approach is to use Docker as shown above")

    return False

if __name__ == "__main__":
    main()