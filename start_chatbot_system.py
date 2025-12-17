#!/usr/bin/env python3
"""
Comprehensive startup script for the Humanoid Robotics Book Chatbot
This script handles all dependencies and starts the full system
"""
import os
import sys
import subprocess
import time
import requests
import signal
import threading
from pathlib import Path

def check_port(port):
    """Check if a port is in use"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def check_qdrant_running():
    """Check if Qdrant is already running on port 6333"""
    try:
        response = requests.get("http://localhost:6333/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def start_qdrant_docker():
    """Start Qdrant using Docker"""
    print("🐳 Attempting to start Qdrant with Docker...")

    # Check if Docker is available
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("❌ Docker is not available or not installed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Docker is not available or not installed")
        return False

    # Check if Qdrant container is already running
    result = subprocess.run(['docker', 'ps', '--format', '"{{.Names}}"'], capture_output=True, text=True)
    if 'qdrant' in result.stdout:
        print("✅ Qdrant container is already running")
        return True

    # Start Qdrant container
    try:
        print("🚀 Starting Qdrant container...")
        subprocess.run([
            'docker', 'run', '-d', '--name', 'qdrant',
            '-p', '6333:6333', '-p', '6334:6334',
            'qdrant/qdrant'
        ], check=True)

        # Wait for Qdrant to be ready
        print("⏳ Waiting for Qdrant to start...")
        for i in range(30):  # Wait up to 30 seconds
            if check_qdrant_running():
                print("✅ Qdrant is ready!")
                return True
            time.sleep(1)

        print("❌ Qdrant failed to start within 30 seconds")
        return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Qdrant container: {e}")
        return False

def install_dependencies():
    """Install required Python dependencies"""
    print("📦 Installing Python dependencies...")

    requirements_file = "docusaurus-book/backend/requirements.txt"
    if not os.path.exists(requirements_file):
        print(f"❌ Requirements file not found: {requirements_file}")
        return False

    try:
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", requirements_file
        ], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False

        print("✅ Dependencies installed successfully")
        return True
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def run_ingestion():
    """Run the ingestion script to load book content"""
    print("📚 Loading book content into vector database...")

    try:
        # Change to backend directory
        original_dir = os.getcwd()
        os.chdir("docusaurus-book/backend")

        # Run ingestion
        result = subprocess.run([
            sys.executable, "../../ingest.py"
        ], capture_output=True, text=True)

        os.chdir(original_dir)  # Change back to original directory

        if result.returncode != 0:
            print(f"⚠️  Ingestion failed: {result.stderr}")
            print("⚠️  This may be due to Qdrant not being available yet. The system will continue.")
            return False

        print("✅ Book content loaded successfully")
        return True
    except Exception as e:
        print(f"⚠️  Error during ingestion: {e}")
        print("⚠️  This may be due to Qdrant not being available yet. The system will continue.")
        return False

def start_backend_server():
    """Start the FastAPI backend server"""
    print("🤖 Starting backend API server...")

    try:
        # Change to backend directory
        original_dir = os.getcwd()
        os.chdir("docusaurus-book/backend")

        # Start the server in a subprocess
        process = subprocess.Popen([
            sys.executable, "-c",
            """
import uvicorn
from main import app
uvicorn.run(app, host="0.0.0.0", port=8000)
            """
        ])

        os.chdir(original_dir)  # Change back to original directory

        # Wait a bit for the server to start
        time.sleep(3)

        # Check if server is running
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend server is running on http://localhost:8000")
                return process
        except requests.exceptions.RequestException:
            pass

        print("⚠️  Backend server may still be starting up...")
        return process
    except Exception as e:
        print(f"❌ Error starting backend server: {e}")
        return None

def start_frontend():
    """Start the Docusaurus frontend"""
    print("🎨 Starting frontend...")

    try:
        # Check if npm is available
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ npm is not available. Please install Node.js and npm.")
            return None

        # Change to docusaurus directory
        original_dir = os.getcwd()
        os.chdir("docusaurus-book")

        # Install frontend dependencies
        print("📦 Installing frontend dependencies...")
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Failed to install frontend dependencies: {result.stderr}")
            os.chdir(original_dir)
            return None

        # Start the frontend in a subprocess
        process = subprocess.Popen(['npx', 'docusaurus', 'start'])

        os.chdir(original_dir)  # Change back to original directory

        # Wait a bit for the frontend to start
        time.sleep(5)

        # Check if frontend is running
        try:
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                print("✅ Frontend is running on http://localhost:3000")
                return process
        except requests.exceptions.RequestException:
            pass

        print("⚠️  Frontend may still be starting up...")
        return process
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return None

def main():
    print("🚀 Starting Humanoid Robotics Book Chatbot System...")
    print("="*60)

    # Check if Qdrant is already running
    if not check_qdrant_running():
        print("🔍 Qdrant not found, attempting to start...")
        if not start_qdrant_docker():
            print("❌ Could not start Qdrant. Please ensure Docker Desktop is running and execute:")
            print("   docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant")
            print("   Then restart this script.")
            return False
    else:
        print("✅ Qdrant is already running")

    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return False

    # Run ingestion to load book content
    run_ingestion()  # This is non-critical, so we continue even if it fails

    # Check if backend is already running
    backend_process = None
    if not check_port(8000):
        backend_process = start_backend_server()
        if not backend_process:
            print("❌ Failed to start backend server")
            return False
    else:
        print("✅ Backend server is already running on port 8000")

    # Check if frontend is already running
    frontend_process = None
    if not check_port(3000):
        frontend_process = start_frontend()
        if not frontend_process:
            print("❌ Failed to start frontend")
            return False
    else:
        print("✅ Frontend is already running on port 3000")

    print("="*60)
    print("🎉 Humanoid Robotics Book Chatbot is now running!")
    print()
    print("📖 Book: http://localhost:3000")
    print("💬 Chat: http://localhost:3000/chat")
    print("🤖 Backend API: http://localhost:8000")
    print("📚 Backend API Docs: http://localhost:8000/docs")
    print()
    print("💡 The system is running. Press Ctrl+C to stop.")
    print("="*60)

    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("👋 System stopped.")
        return True

if __name__ == "__main__":
    main()