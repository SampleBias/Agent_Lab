# Gemini Model Selection for PyMOL Learning Agent

## Current Model: `gemini-2.5-pro`

### Why Gemini 2.5 Pro?

This agent requires sophisticated capabilities that make **Gemini 2.5 Pro** the optimal choice:

#### 1. **Function Calling & Tool Orchestration** ⭐
- **Requirement**: The agent needs to orchestrate multiple tool categories:
  - PyMOL Tools (command execution)
  - Vision Tools (image analysis)
  - Desktop Tools (GUI automation)
  - GUI Inspector Tools (accessibility)
- **Why Pro**: Superior function calling capabilities ensure reliable tool selection and execution in complex scenarios

#### 2. **Multimodal & Vision Analysis** 🖼️
- **Requirement**: Analyze molecular images, screenshots, and visualizations
- **Why Pro**: Enhanced multimodal understanding provides better accuracy for vision-based tasks

#### 3. **Complex Reasoning** 🧠
- **Requirement**: Understand natural language commands about molecular visualization and translate them to PyMOL operations
- **Why Pro**: Advanced reasoning capabilities handle complex, multi-step instructions better

#### 4. **Large Context Window** 📚
- **Requirement**: Maintain conversation history and context across multiple interactions
- **Why Pro**: 1 million token context window (vs 1M for Flash, but Pro uses it more effectively)

#### 5. **Agent Development** 🤖
- **Requirement**: Act as an intelligent agent that can plan, reason, and execute multi-step workflows
- **Why Pro**: Designed for complex agentic tasks requiring deep reasoning

## Model Comparison

| Model | Best For | Function Calling | Multimodal | Context | Cost |
|-------|----------|------------------|------------|---------|------|
| **gemini-2.5-pro** | ✅ Complex reasoning, agents | ⭐⭐⭐ Excellent | ⭐⭐⭐ Excellent | 1M tokens | Higher |
| **gemini-2.5-flash** | Balanced performance/cost | ⭐⭐ Good | ⭐⭐ Good | 1M tokens | Lower |
| **gemini-2.5-flash-lite** | High throughput, cost-sensitive | ⭐⭐ Good | ⭐⭐ Good | 1M tokens | Lowest |
| **gemini-3-pro** | Latest, advanced reasoning | ⭐⭐⭐ Excellent | ⭐⭐⭐ Excellent | Large | Highest |

## Alternative Models

If you need to optimize for cost, you can switch to:

### `gemini-2.5-flash`
- **When to use**: If cost is a primary concern and you're willing to trade some reasoning quality
- **Trade-offs**: Slightly less reliable tool orchestration, but still very capable
- **How to switch**: Change the `model` parameter in `agent.py` and `main.py`

### `gemini-2.5-flash-lite`
- **When to use**: For high-volume, simple interactions where cost is critical
- **Trade-offs**: May struggle with complex multi-tool orchestration
- **Not recommended** for this agent due to complexity requirements

## Model Capabilities Summary

### All Models Support:
- ✅ Function calling (tool use)
- ✅ Multimodal input (text, images, video, audio)
- ✅ Structured outputs
- ✅ Batch API
- ✅ Caching

### Pro Advantages:
- 🎯 Better tool selection and orchestration
- 🎯 Superior reasoning for complex commands
- 🎯 Enhanced multimodal understanding
- 🎯 More reliable agent behavior

## References

- [Google Gemini Models Documentation](https://ai.google.dev/models/gemini)
- [Gemini API Function Calling Guide](https://ai.google.dev/gemini-api/docs/function-calling)
- [Model Comparison Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/models)

## Configuration

The model is configured in:
- `agent.py`: Line 174 - `PyMOLAgent.__init__()`
- `main.py`: Line 22 - `IntegratedPyMOLAgent.__init__()`

To change the model, update the default parameter:
```python
def __init__(self, api_key: str = None, model: str = "gemini-2.5-pro"):
```

Or set via environment variable:
```bash
export AGENT_MODEL=gemini-2.5-pro
```

