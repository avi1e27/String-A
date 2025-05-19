@echo off
echo 🎨 Setting up String Art Generator...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is required but not installed.
    echo Please install Python 3.7 or higher and try again.
    pause
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv string_art_env

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call string_art_env\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📥 Installing dependencies...
pip install -r requirements.txt

echo ✅ Installation complete!
echo.
echo 🚀 To run the application:
echo 1. Activate the virtual environment: string_art_env\Scripts\activate.bat
echo 2. Run the app: streamlit run app.py
echo.
echo 🌐 The app will open in your default web browser.
echo 💡 Use Ctrl+C to stop the application.
pause
