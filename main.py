"""
Phase 3: Integration and Logic - Complete PyMOL Learning Agent
This module integrates all tools and provides the complete agent orchestration.
"""

import asyncio
import os
import sys
from pathlib import Path

# Import our agent foundation and tools
from agent import PyMOLAgent
from pymol_tools import register_pymol_tools
from vision_tools import register_vision_tools
from desktop_tools import register_desktop_tools
from gui_inspector import register_gui_inspector_tools


class IntegratedPyMOLAgent:
    """Complete PyMOL Learning Agent with all tools integrated."""
    
    def __init__(self, api_key: str = None, model: str = "gemini-2.5-pro"):
        """Initialize the integrated agent with all tools."""
        
        # Initialize the base agent
        self.agent = PyMOLAgent(api_key=api_key, model=model)
        
        # Register all tool categories
        self._register_all_tools()
        
        # Enhanced system instruction for the integrated agent
        self.agent.system_instruction = """
        You are the PyMOL Learning Agent - an advanced AI assistant designed to help users 
        understand and control PyMOL molecular visualization software through natural language.
        
        CORE CAPABILITIES:
        - Molecular visualization and analysis using PyMOL
        - Vision analysis of molecular images
        - Desktop automation for GUI interactions
        - GUI inspection and accessibility
        - Memory management for contextual conversations
        
        AVAILABLE TOOLS:
        1. PyMOL Tools: Execute commands, load structures, set representations, color molecules
        2. Vision Tools: Analyze images, annotate, compare molecular visualizations
        3. Desktop Tools: Control mouse/keyboard, manage windows, take screenshots
        4. GUI Inspector: Examine interface elements, find clickable elements
        
        WORKFLOW PRINCIPLES:
        1. Always understand the user's intent before taking action
        2. Use vision tools when analyzing molecular structures or screenshots
        3. Use desktop tools when you need to interact with PyMOL's GUI directly
        4. Use GUI inspector to understand the current interface state
        5. Remember previous interactions to provide contextual assistance
        6. Explain your actions and reasoning to the user
        
        BEST PRACTICES:
        - Start by asking clarifying questions if the user's request is ambiguous
        - Use screenshots and vision analysis to understand the current state
        - Combine multiple tools when necessary (e.g., screenshot + vision analysis)
        - Provide educational explanations alongside technical actions
        - Remember molecular structures and preferences for future sessions
        
        SAFETY:
        - Always ask for confirmation before performing destructive operations
        - Warn users before overwriting files or making significant changes
        - Ensure PyMOL commands are safe and won't crash the application
        
        Your goal is to make PyMOL accessible and educational for users at all levels.
        """
    
    def _register_all_tools(self):
        """Register all tool categories with the agent."""
        print("Registering PyMOL tools...")
        register_pymol_tools(self.agent)
        
        print("Registering vision analysis tools...")
        register_vision_tools(self.agent)
        
        print("Registering desktop control tools...")
        register_desktop_tools(self.agent)
        
        print("Registering GUI inspector tools...")
        register_gui_inspector_tools(self.agent)
        
        print(f"✓ All tools registered. Total tools: {len(self.agent.tool_registry.tools)}")
    
    async def process_request(self, user_input: str, temperature: float = 0.1) -> str:
        """Process a user request with full agent capabilities."""
        return await self.agent.process_message(user_input, temperature)
    
    def get_agent_status(self) -> str:
        """Get comprehensive status of the agent."""
        memory_summary = self.agent.get_memory_summary()
        tool_count = len(self.agent.tool_registry.tools)
        
        return f"""PyMOL Learning Agent Status:
{memory_summary}
Active Model: {self.agent.model}
Temperature: {0.1}
System Ready: ✓"""
    
    async def interactive_session(self):
        """Start an interactive session with the agent."""
        print("=" * 60)
        print("PyMOL Learning Agent - Interactive Session")
        print("Type 'quit' to exit, 'status' for agent status")
        print("=" * 60)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if user_input.lower() == 'status':
                    print(f"\nAgent Status:\n{self.get_agent_status()}")
                    continue
                
                if not user_input:
                    continue
                
                print("Agent: ", end="", flush=True)
                response = await self.process_request(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\nSession interrupted. Type 'quit' to exit.")
            except Exception as e:
                print(f"\nError: {e}")


# Demo and testing functions
async def demo_basic_functionality():
    """Demonstrate basic agent functionality."""
    print("🧪 Running basic functionality demo...")
    
    agent = IntegratedPyMOLAgent()
    print(f"\nAgent initialized: {agent.get_agent_status()}")
    
    demo_queries = [
        "Hello! What can you help me with regarding molecular visualization?",
        "Can you explain what PyMOL is and what it's used for?",
        "How would I load a protein structure in PyMOL?",
        "What are the different ways to visualize molecules?",
        "Can you help me understand molecular representations?"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n--- Query {i} ---")
        print(f"User: {query}")
        print("Agent: ", end="", flush=True)
        response = await agent.process_request(query)
        print(response)


async def demo_tool_integration():
    """Demonstrate tool integration capabilities."""
    print("\n🔧 Running tool integration demo...")
    
    agent = IntegratedPyMOLAgent()
    
    # Test individual tool categories
    test_queries = [
        # Desktop/GUI testing
        "Can you take a screenshot of my current screen?",
        "What windows do I have open on my desktop?",
        
        # Vision testing (would need actual images)
        "How would you analyze a molecular image if I provided one?",
        
        # PyMOL testing
        "What PyMOL command would I use to load a PDB file named 'protein.pdb'?",
        "How do I set the representation to cartoon in PyMOL?",
        
        # Complex workflow
        "Describe the workflow for loading a protein, setting it to cartoon representation, and coloring it by secondary structure."
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Tool Test {i} ---")
        print(f"User: {query}")
        print("Agent: ", end="", flush=True)
        response = await agent.process_request(query)
        print(response)


async def main():
    """Main function with options for different modes."""
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        print("\nPyMOL Learning Agent - Choose mode:")
        print("1. Interactive session")
        print("2. Basic demo")
        print("3. Tool integration demo")
        
        choice = input("\nEnter choice (1-3): ").strip()
        mode_map = {"1": "interactive", "2": "basic", "3": "tools"}
        mode = mode_map.get(choice, "interactive")
    
    # Check for API key (support both GEMINI_API_KEY and GOOGLE_API_KEY)
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY or GOOGLE_API_KEY environment variable is required")
        print("Get your API key from: https://aistudio.google.com/apikey")
        print("Set it with: export GEMINI_API_KEY=your_key_here")
        print("Or add it to your .env file: GEMINI_API_KEY=your_key_here")
        return
    
    try:
        if mode == "interactive":
            agent = IntegratedPyMOLAgent()
            await agent.interactive_session()
        
        elif mode == "basic":
            await demo_basic_functionality()
        
        elif mode == "tools":
            await demo_tool_integration()
        
        else:
            print(f"Unknown mode: {mode}")
    
    except KeyboardInterrupt:
        print("\nSession interrupted.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())