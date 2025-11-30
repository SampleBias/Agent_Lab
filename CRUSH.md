# Agent Lab - Development Guide

## Project Overview
This is an Agent Development Kit (ADK) laboratory focused on building a PyMOL Learning Agent that can translate natural language commands into PyMOL application actions.

## Development Commands

### Build and Setup
```bash
# Full setup with virtual environment
./setup.sh

# Manual setup
pip install -r requirements.txt
pip install Pillow pyautogui pygetwindow  # Optional dependencies
```

### Testing and Running
```bash
# Interactive session (requires GEMINI_API_KEY)
python main.py interactive

# Test basic functionality
python main.py basic

# Test tool integration
python main.py tools

# Run specific test
pytest tests/  # When tests are implemented
```

### Environment Setup
```bash
# Copy environment template
cp .env.example .env
# Edit .env with your GEMINI_API_KEY from https://aistudio.google.com/apikey
```

## Code Style Guidelines

### Core Architecture
- **Base Agent**: Use `PyMOLAgent` class for core orchestration
- **Memory System**: Implement both short-term and long-term memory using `MemorySystem`
- **Tool Registration**: Use modular registration pattern with `register_*_tools()` functions
- **Function Declarations**: Auto-generate from Python functions using Gemini SDK patterns

### Tool Development Patterns
- **Function Naming**: Use descriptive names (`load_molecule`, `analyze_molecular_image`)
- **Error Handling**: Always return `dict` with `success: bool` and `error: str` on failure
- **Type Hints**: Include full type annotations for all function parameters and returns
- **Documentation**: Use Google-style docstrings with Args/Returns sections
- **Validation**: Validate inputs before executing operations

### Integration Guidelines
- **Agent Composition**: Build `IntegratedPyMOLAgent` by composing base agent + tools
- **System Instructions**: Enhanced prompts that describe all available capabilities
- **Tool Orchestration**: Agent should select appropriate tools based on user intent
- **Memory Context**: Include recent memory in prompts for contextual conversations

### Python Standards
- **Python 3.8+**: Target modern Python features
- **Async/Await**: Use async for agent processing and tool calls
- **Environment Variables**: Use `os.getenv()` for configuration with `.env` file
- **Pathlib**: Use `pathlib.Path` for file operations

### Error Handling
- **Graceful Degradation**: Tools should work independently if dependencies missing
- **User-Friendly Messages**: Clear error descriptions with suggestions
- **Logging**: Use structured error reporting for debugging
- **Timeouts**: Implement timeouts for external operations

## Agent Development Principles
- Tools should be designed for reliability and error handling
- Vision and accessibility tools should complement each other
- Orchestration logic should prioritize appropriate tool selection
- Natural language understanding should map precisely to PyMOL commands
- Always validate operations before execution
- Provide educational context alongside technical actions

## Next Development Steps
- Set up Google ADK framework ✅
- Initialize agent project ✅
- Implement memory systems ✅
- Develop PyMOL command execution tools ✅
- Implement vision analysis capabilities ✅
- Add desktop automation tools ✅
- Create GUI inspection tools ✅
- Integrate all components in unified agent ✅
- Add comprehensive testing and documentation ✅

## API Key Required
You need to set your `GEMINI_API_KEY` environment variable before running the agent:
```bash
export GEMINI_API_KEY=your_key_here
# Or add to .env file
```
Get your API key from: https://aistudio.google.com/apikey