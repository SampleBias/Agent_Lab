# PyMOL Learning Agent

A comprehensive AI agent built with Google's Gemini API that can understand natural language commands and translate them into actions within the PyMOL molecular visualization application.

## 🚀 Features

### Core Capabilities
- **Natural Language Understanding**: Parse and understand commands about molecular visualization
- **PyMOL Integration**: Execute PyMOL commands and manage molecular structures
- **Vision Analysis**: Analyze molecular images and screenshots
- **Desktop Automation**: Control PyMOL GUI through mouse and keyboard automation
- **GUI Inspection**: Understand and interact with interface elements
- **Memory Management**: Maintain context and learn from interactions

### Tool Categories
1. **PyMOL Tools**: Load structures, set representations, color molecules, save images
2. **Vision Tools**: Analyze images, annotate, compare molecular visualizations
3. **Desktop Tools**: Control mouse/keyboard, manage windows, take screenshots
4. **GUI Inspector**: Examine interface elements, find clickable elements

## 📋 Requirements

- Python 3.8+
- Google Gemini API key
- PyMOL (for molecular visualization operations)
- Optional: PIL/Pillow for image processing
- Optional: pyautogui, pygetwindow for desktop automation

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Agent_Lab
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install optional dependencies for full functionality**
```bash
pip install Pillow pyautogui pygetwindow
```

4. **Set up your environment**
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

5. **Get your Gemini API key**
- Visit [Google AI Studio](https://aistudio.google.com/apikey)
- Create a new API key
- Add it to your `.env` file or environment variables

## 🎯 Quick Start

### Interactive Mode
```bash
python main.py interactive
```

### Demo Mode
```bash
python main.py basic    # Basic functionality demo
python main.py tools    # Tool integration demo
```

### Programmatic Usage
```python
from main import IntegratedPyMOLAgent

async def use_agent():
    agent = IntegratedPyMOLAgent()
    response = await agent.process_request("How do I load a protein structure in PyMOL?")
    print(response)

# Run the agent
import asyncio
asyncio.run(use_agent())
```

## 📖 Usage Examples

### Basic PyMOL Commands
```
User: Load the protein file called "1ubq.pdb"
User: Show the protein as a cartoon representation
User: Color the molecule by secondary structure
User: Save the current view as "protein_view.png"
```

### Vision Analysis
```
User: Analyze this molecular image and tell me what you see
User: Compare these two protein structures
User: Annotate the active site in this image
```

### Desktop Automation
```
User: Open PyMOL and maximize the window
User: Click on the "File" menu
User: Take a screenshot of the current PyMOL view
```

## 🏗️ Architecture

### Phase 1: Foundation ✅
- Agent orchestration using Gemini API
- Memory management (short-term and long-term)
- Function calling framework
- Session handling

### Phase 2: Tool Development ✅
- **PyMOL Command Executor**: Execute PyMOL commands safely
- **Vision Analyzer**: Analyze molecular images using computer vision
- **Desktop Controller**: Automate GUI interactions
- **GUI Inspector**: Examine interface elements and accessibility

### Phase 3: Integration ✅
- Complete tool orchestration
- Enhanced system instructions
- Error handling and recovery
- Interactive session management

## 🔧 Configuration

### Environment Variables
```bash
GEMINI_API_KEY=your_api_key_here
PYMOL_PATH=/usr/local/bin/pymol
AGENT_MODEL=gemini-2.5-pro
AGENT_TEMPERATURE=0.1
```

### Agent Settings
- **Model**: Gemini 2.5 Pro (optimized for function calling, complex reasoning, and multimodal tasks)
  - **Why Pro?**: This agent requires advanced reasoning for tool orchestration, vision analysis, and understanding complex PyMOL commands. Pro provides:
    - Superior function calling capabilities for multi-tool orchestration
    - Enhanced multimodal understanding for vision analysis
    - 1M token context window for maintaining conversation history
    - Better reasoning for complex natural language commands
- **Temperature**: 0.1 (for consistent responses)
- **Memory**: Configurable short-term and long-term storage
- **Tools**: Modular registration system

**Note**: If cost is a primary concern, you can switch to `gemini-2.5-flash` which offers a good balance, but Pro is recommended for optimal agent performance.

## 🧪 Testing

### Run All Demos
```bash
python main.py basic    # Test basic functionality
python main.py tools    # Test tool integration
```

### Test Individual Components
```python
# Test PyMOL tools
from pymol_tools import execute_pymol_command
result = execute_pymol_command("print('Hello PyMOL')")
print(result)

# Test vision tools
from vision_tools import analyze_molecular_image
result = analyze_molecular_image("protein_image.png")
print(result)
```

## 🔒 Safety Features

- **Command Validation**: PyMOL commands are validated before execution
- **Timeout Protection**: Commands have configurable timeouts
- **Confirmation Prompts**: Destructive actions require user confirmation
- **Error Handling**: Comprehensive error recovery and reporting
- **Memory Protection**: Sensitive information is not stored in long-term memory

## 🚧 Limitations

- PyMOL must be installed and accessible via command line
- Desktop automation requires PyMOL to be visible on screen
- Vision analysis depends on image quality and resolution
- Some advanced features may require additional library installations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini API for the core AI capabilities
- PyMOL team for the molecular visualization software
- Open-source community for the automation and vision libraries

## 📞 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Report bugs and feature requests via GitHub Issues
- **API Keys**: Get help at [Google AI Studio](https://aistudio.google.com)

---

**Note**: You need to set your `GEMINI_API_KEY` environment variable before running the agent. Get your key from [Google AI Studio](https://aistudio.google.com/apikey).