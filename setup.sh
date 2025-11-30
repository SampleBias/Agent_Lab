#!/bin/bash
# PyMOL Learning Agent Setup Script

echo "🧪 Setting up PyMOL Learning Agent..."

# Check Python version
python_version=$(python3 --version 2>&1)
echo "Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install optional dependencies
echo "🔍 Installing optional dependencies for full functionality..."
pip install Pillow pyautogui pygetwindow || echo "⚠️  Some optional dependencies failed to install"

# Check for PyMOL
echo "🔬 Checking for PyMOL installation..."
if command -v pymol &> /dev/null; then
    echo "✅ PyMOL found at $(which pymol)"
    pymol_version=$(pymol -cq 2>&1 | head -n 1 || echo "Unknown version")
    echo "PyMOL version: $pymol_version"
else
    echo "⚠️  PyMOL not found in PATH"
    echo "Please install PyMOL from https://pymol.org/"
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your GEMINI_API_KEY"
fi

# Check for API key
if [ -f ".env" ]; then
    if grep -q "your_api_key_here" .env; then
        echo "❌ Please set your GEMINI_API_KEY in .env file"
        echo "Get your key from: https://aistudio.google.com/apikey"
    else
        echo "✅ API key is set in .env file"
    fi
else
    echo "❌ .env file not found. Please create it from .env.example"
fi

# Run basic test
echo "🧪 Running basic agent test..."
python3 -c "
import sys
try:
    from agent import PyMOLAgent
    print('✅ Agent imports successfully')
    
    from pymol_tools import register_pymol_tools
    from vision_tools import register_vision_tools  
    from desktop_tools import register_desktop_tools
    from gui_inspector import register_gui_inspector_tools
    print('✅ All tool modules import successfully')
    
    from main import IntegratedPyMOLAgent
    print('✅ Integrated agent imports successfully')
    
    # Test memory system
    from agent import MemorySystem
    memory = MemorySystem()
    memory.add_short_term('Test message', importance=1.0)
    print('✅ Memory system working')
    
    print('🎉 All basic tests passed!')
    
except Exception as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
" 2>/dev/null || echo "❌ Basic test failed - check your installation"

echo ""
echo "🚀 Setup complete! Next steps:"
echo "1. Set your GEMINI_API_KEY in .env file"
echo "2. Run: python main.py interactive"
echo "3. Or try demos: python main.py basic"
echo ""
echo "For more info, see README.md"