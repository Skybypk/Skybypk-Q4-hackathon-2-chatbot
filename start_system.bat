@echo off
REM Startup script for the Humanoid Robotics Book with Chatbot
REM This script will start both the Docusaurus frontend and the RAG backend

echo 🚀 Starting Humanoid Robotics Book with Chatbot System...

REM Function to check if a port is in use
:check_port
    netstat -an | findstr :%1 >nul
    if %errorlevel% equ 0 (
        exit /b 0
    ) else (
        exit /b 1
    )

REM Start the backend
echo 📦 Starting RAG backend server...

REM Navigate to backend directory
cd docusaurus-book\backend

REM Check if Qdrant is running, if not start it
call :check_port 6333
if %errorlevel% neq 0 (
    echo 🔍 Qdrant not found, starting Qdrant container...
    docker --version >nul 2>&1
    if %errorlevel% equ 0 (
        REM Check if qdrant container is already running
        docker ps --format "table {{.Names}}" | findstr qdrant >nul
        if %errorlevel% neq 0 (
            echo 🐳 Starting Qdrant container...
            docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant
            timeout /t 5 /nobreak >nul
        ) else (
            echo ✅ Qdrant container is already running
        )
    ) else (
        echo ⚠️  Docker not found. Please install Docker to run Qdrant.
        echo    Or start Qdrant manually on port 6333
        pause
        exit /b 1
    )
) else (
    echo ✅ Qdrant is already running on port 6333
)

REM Check if backend is already running
call :check_port 8000
if %errorlevel% equ 0 (
    echo ⚠️  Backend server appears to be already running on port 8000
) else (
    echo 🔧 Installing backend dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install backend dependencies
        pause
        exit /b 1
    )

    echo 📊 Setting up Qdrant and indexing book content...
    python setup_qdrant.py
    if %errorlevel% neq 0 (
        echo ❌ Failed to setup Qdrant
        pause
        exit /b 1
    )

    echo 🤖 Starting RAG API server in a new window...
    start "RAG Backend" cmd /k "python start_rag_system.py"

    REM Wait a bit for the server to start
    timeout /t 5 /nobreak >nul
    echo ✅ Backend server started successfully
)

REM Navigate back to main directory and start the frontend
cd ..\..

REM Check if frontend is already running
call :check_port 3000
if %errorlevel% equ 0 (
    echo ⚠️  Frontend appears to be already running on port 3000
) else (
    echo 🔧 Installing frontend dependencies...
    cd docusaurus-book
    npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install frontend dependencies
        pause
        exit /b 1
    )

    echo 🎨 Starting Docusaurus development server in a new window...
    start "Docusaurus Frontend" cmd /k "npx docusaurus start"

    REM Wait a bit for the server to start
    timeout /t 5 /nobreak >nul
    echo ✅ Frontend started successfully
)

echo.
echo 🎉 Humanoid Robotics Book with Chatbot is now running!
echo.
echo 📖 Book: http://localhost:3000
echo 💬 Chat: http://localhost:3000/chat
echo 🤖 Backend API: http://localhost:8000
echo 📚 Backend API Docs: http://localhost:8000/docs
echo.
echo The system is running in separate windows.
echo Close those windows to stop the system.
echo.
pause