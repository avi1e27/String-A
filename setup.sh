#!/bin/bash

# String Art Generator Setup Script

echo "🎨 Setting up String Art Generator..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.7 or higher and try again."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.7"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python $python_version found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv string_art_env

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source string_art_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Installation complete!"
echo ""
echo "🚀 To run the application:"
echo "1. Activate the virtual environment: source string_art_env/bin/activate"
echo "2. Run the app: streamlit run app.py"
echo ""
echo "🌐 The app will open in your default web browser."
echo "💡 Use Ctrl+C to stop the application."
