"""
PyMOL Learning Agent - Phase 1 Foundation
Agent orchestration and environment setup using Google Gemini API

This module implements the core agent infrastructure with:
- Memory management (short-term and long-term)
- Function calling orchestration
- Tool registration and management
- Session handling
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import types
from pydantic import BaseModel

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


@dataclass
class MemoryItem:
    """Represents a single memory item with timestamp and content."""
    timestamp: datetime
    content: str
    importance: float = 1.0
    tags: List[str] = field(default_factory=list)


class MemorySystem:
    """Manages both short-term and long-term memory for the agent."""
    
    def __init__(self, max_short_term: int = 10, memory_file: str = "memory.json"):
        self.max_short_term = max_short_term
        self.memory_file = Path(memory_file)
        self.short_term: List[MemoryItem] = []
        self.long_term: List[MemoryItem] = []
        self._load_memory()
    
    def add_short_term(self, content: str, importance: float = 1.0, tags: List[str] = None):
        """Add item to short-term memory."""
        item = MemoryItem(
            timestamp=datetime.now(),
            content=content,
            importance=importance,
            tags=tags or []
        )
        self.short_term.append(item)
        
        # Keep only recent items in short-term memory
        if len(self.short_term) > self.max_short_term:
            # Move oldest items to long-term if important enough
            oldest = self.short_term.pop(0)
            if oldest.importance >= 0.7:
                self.long_term.append(oldest)
        
        self._save_memory()
    
    def add_long_term(self, content: str, importance: float = 1.0, tags: List[str] = None):
        """Add item directly to long-term memory."""
        item = MemoryItem(
            timestamp=datetime.now(),
            content=content,
            importance=importance,
            tags=tags or []
        )
        self.long_term.append(item)
        self._save_memory()
    
    def search_memory(self, query: str, limit: int = 5) -> List[MemoryItem]:
        """Search through both memory types for relevant content."""
        all_memories = self.short_term + self.long_term
        
        # Simple keyword matching - can be enhanced with embeddings
        relevant = [mem for mem in all_memories 
                   if any(word.lower() in mem.content.lower() 
                         for word in query.split())]
        
        return sorted(relevant, key=lambda x: x.importance, reverse=True)[:limit]
    
    def get_context(self, limit: int = 5) -> str:
        """Get recent context from short-term memory."""
        if not self.short_term:
            return "No previous context."
        
        context_items = self.short_term[-limit:]
        return "\n".join([f"[{mem.timestamp.strftime('%H:%M')}] {mem.content}" 
                         for mem in context_items])
    
    def _load_memory(self):
        """Load long-term memory from file."""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.long_term = [
                        MemoryItem(
                            timestamp=datetime.fromisoformat(item['timestamp']),
                            content=item['content'],
                            importance=item['importance'],
                            tags=item['tags']
                        )
                        for item in data
                    ]
            except Exception as e:
                print(f"Error loading memory: {e}")
    
    def _save_memory(self):
        """Save long-term memory to file."""
        try:
            data = []
            for mem in self.long_term:
                data.append({
                    'timestamp': mem.timestamp.isoformat(),
                    'content': mem.content,
                    'importance': mem.importance,
                    'tags': mem.tags
                })
            
            with open(self.memory_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")


class ToolRegistry:
    """Registry for managing agent tools and functions."""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self.tool_declarations: List[Dict] = []
    
    def register_tool(self, name: str, func: Callable, description: str = None):
        """Register a tool with the agent."""
        self.tools[name] = func
        
        # Auto-generate function declaration from function
        if hasattr(func, '__doc__') and description is None:
            description = func.__doc__
        
        # Create function declaration for Gemini API
        self.tool_declarations.append({
            "name": name,
            "description": description or f"Tool for {name}",
            "parameters": self._extract_parameters(func)
        })
    
    def _extract_parameters(self, func: Callable) -> Dict:
        """Extract parameters from function signature."""
        # This is a simplified version - can be enhanced with introspection
        return {
            "type": "object",
            "properties": {},
            "required": []
        }
    
    def get_tools_config(self) -> List[types.Tool]:
        """Get tools configuration for Gemini API."""
        return [types.Tool(function_declarations=[decl]) 
                for decl in self.tool_declarations]


class PyMOLAgent:
    """Main PyMOL Learning Agent with orchestration capabilities."""
    
    def __init__(self, api_key: str = None, model: str = "gemini-2.5-pro"):
        # Check for API key in multiple environment variables (google-genai supports both)
        # The google-genai library can read from GOOGLE_API_KEY automatically, but we'll
        # explicitly pass it to ensure it's used correctly
        self.api_key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
        # Strip whitespace that might be in .env file
        if self.api_key:
            self.api_key = self.api_key.strip()
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY or GOOGLE_API_KEY environment variable is required")
        
        # Validate API key format
        if not self.api_key.startswith("AIza"):
            raise ValueError(
                f"Invalid API key format. API keys should start with 'AIza'. "
                f"Got: {self.api_key[:10]}... (length: {len(self.api_key)})"
            )
        
        # Initialize client with explicit API key
        # Note: google-genai Client can also read from GOOGLE_API_KEY env var automatically,
        # but we pass it explicitly to ensure the correct key is used
        # Also set it as GOOGLE_API_KEY in case the library checks that first
        os.environ["GOOGLE_API_KEY"] = self.api_key
        
        try:
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            error_str = str(e)
            # Provide detailed error information
            error_details = (
                f"Failed to initialize Gemini client.\n"
                f"Error: {error_str}\n\n"
                f"API Key Info:\n"
                f"  - First 20 chars: {self.api_key[:20]}...\n"
                f"  - Length: {len(self.api_key)} (expected ~39)\n"
                f"  - Format valid: {self.api_key.startswith('AIza')}\n\n"
            )
            
            if "API key expired" in error_str or "API_KEY_INVALID" in error_str:
                error_details += (
                    "🔍 Diagnosis: API Key Authentication Failed\n\n"
                    "Possible causes:\n"
                    "  1. API key has expired (check expiration date in Google Cloud Console)\n"
                    "  2. API key is invalid or was revoked\n"
                    "  3. Gemini API is not enabled for this key/project\n"
                    "  4. API key has IP/domain restrictions blocking your access\n"
                    "  5. API key was created but not properly activated\n\n"
                    "Solutions:\n"
                    "  1. Visit https://aistudio.google.com/apikey\n"
                    "  2. Create a NEW API key (don't reuse old keys)\n"
                    "  3. Ensure 'Generative Language API' is enabled\n"
                    "  4. Check API key restrictions in Google Cloud Console\n"
                    "  5. Update .env file: GEMINI_API_KEY=your_new_key\n"
                    "  6. Run test script: python test_api_key.py\n"
                )
            elif "400" in error_str or "INVALID_ARGUMENT" in error_str:
                error_details += (
                    "🔍 Diagnosis: Invalid Request\n"
                    "This might indicate:\n"
                    "  - Model name issue (check if 'gemini-2.5-pro' is available)\n"
                    "  - API version mismatch\n"
                    "  - Request format issue\n"
                )
            
            raise ValueError(error_details) from e
        self.model = model
        self.memory = MemorySystem()
        self.tool_registry = ToolRegistry()
        self.session_history = []
        
        # System instruction for the agent
        self.system_instruction = """
        You are a PyMOL Learning Agent - an intelligent assistant that helps users 
        understand and control PyMOL molecular visualization software.
        
        Your capabilities include:
        - Understanding natural language commands about molecular visualization
        - Executing PyMOL commands and operations
        - Explaining PyMOL concepts and features
        - Providing guidance on molecular analysis and visualization techniques
        
        You have access to specialized tools for interacting with PyMOL and analyzing 
        molecular structures. Always use these tools when appropriate rather than 
        trying to execute PyMOL commands directly in your responses.
        
        When users ask about molecular structures, visualization, or PyMOL operations,
        use your tools to provide accurate and helpful assistance.
        """
        
        self._register_base_tools()
    
    def _register_base_tools(self):
        """Register basic tools for the agent."""
        
        def echo_message(message: str) -> dict:
            """Echo a message back to the user (testing tool)."""
            return {"message": f"Echo: {message}"}
        
        self.tool_registry.register_tool(
            "echo_message", 
            echo_message, 
            "Echo a message for testing purposes"
        )
    
    async def process_message(self, message: str, temperature: float = 0.1) -> str:
        """Process a user message and generate response."""
        # Add to memory
        self.memory.add_short_term(f"User: {message}", importance=0.8)
        
        # Get context
        context = self.memory.get_context()
        
        # Prepare content
        contents = [
            types.Content(
                role="user", 
                parts=[types.Part(text=f"Context:\n{context}\n\nUser message: {message}")]
            )
        ]
        
        # Configure generation
        config = types.GenerateContentConfig(
            temperature=temperature,
            system_instruction=self.system_instruction,
            tools=self.tool_registry.get_tools_config()
        )
        
        try:
            # Generate response
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=config
            )
            
            # Handle function calls
            if response.candidates[0].content.parts[0].function_call:
                return await self._handle_function_calls(response, contents)
            
            # Get text response
            response_text = response.text
            
            # Add to memory
            self.memory.add_short_term(f"Agent: {response_text}", importance=0.9)
            
            return response_text
            
        except Exception as e:
            error_str = str(e)
            # Provide helpful error messages for common API key issues
            if "API key expired" in error_str or "API_KEY_INVALID" in error_str:
                error_msg = (
                    f"❌ API Key Error: {error_str}\n\n"
                    "This usually means:\n"
                    "1. Your API key has expired - get a new one from https://aistudio.google.com/apikey\n"
                    "2. Your API key is invalid - verify it's correct in your .env file\n"
                    "3. Your API key doesn't have the required permissions\n\n"
                    "To fix:\n"
                    "- Visit https://aistudio.google.com/apikey to create/renew your API key\n"
                    "- Update your .env file with: GEMINI_API_KEY=your_new_key_here\n"
                    "- Make sure the key starts with 'AIza'"
                )
            else:
                error_msg = f"Error processing message: {error_str}"
            
            self.memory.add_short_term(error_msg, importance=1.0)
            return error_msg
    
    async def _handle_function_calls(self, response, contents) -> str:
        """Handle function calls from the model."""
        function_calls = []
        
        # Extract function calls
        for part in response.candidates[0].content.parts:
            if part.function_call:
                function_calls.append(part.function_call)
        
        # Execute function calls
        results = []
        for call in function_calls:
            tool_name = call.name
            args = call.args
            
            if tool_name in self.tool_registry.tools:
                try:
                    result = self.tool_registry.tools[tool_name](**args)
                    results.append({
                        "name": tool_name,
                        "response": result
                    })
                except Exception as e:
                    results.append({
                        "name": tool_name,
                        "response": {"error": str(e)}
                    })
        
        # Send results back to model
        function_response_parts = [
            types.Part.from_function_response(
                name=result["name"],
                response=result["response"]
            )
            for result in results
        ]
        
        # Add to conversation
        contents.append(response.candidates[0].content)
        contents.append(types.Content(role="user", parts=function_response_parts))
        
        # Get final response
        final_response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.1,
                system_instruction=self.system_instruction,
                tools=self.tool_registry.get_tools_config()
            )
        )
        
        final_text = final_response.text
        self.memory.add_short_term(f"Agent: {final_text}", importance=0.9)
        
        return final_text
    
    def add_tool(self, name: str, func: Callable, description: str = None):
        """Add a new tool to the agent."""
        self.tool_registry.register_tool(name, func, description)
    
    def get_memory_summary(self) -> str:
        """Get a summary of agent's memory state."""
        return f"Short-term memory: {len(self.memory.short_term)} items\n" \
               f"Long-term memory: {len(self.memory.long_term)} items\n" \
               f"Registered tools: {len(self.tool_registry.tools)}"


# Example usage and testing
async def main():
    """Main function for testing the agent."""
    # Note: Make sure to set GEMINI_API_KEY in your environment
    
    try:
        agent = PyMOLAgent()
        print("PyMOL Learning Agent initialized successfully!")
        print(agent.get_memory_summary())
        
        # Test the agent
        test_messages = [
            "Hello! Can you help me learn about PyMOL?",
            "Can you echo the message 'testing the agent'?",
            "What can you help me with regarding molecular visualization?"
        ]
        
        for msg in test_messages:
            print(f"\nUser: {msg}")
            response = await agent.process_message(msg)
            print(f"Agent: {response}")
        
    except ValueError as e:
        if "GEMINI_API_KEY" in str(e):
            print("Please set your GEMINI_API_KEY environment variable")
            print("Get your API key from: https://aistudio.google.com/apikey")
        else:
            print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())