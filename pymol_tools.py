"""
Phase 2: Tool Development - PyMOL Command Executor Tool
This module provides tools for executing PyMOL commands and operations.
"""

import subprocess
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class PyMOLCommandExecutor:
    """Handles execution of PyMOL commands and manages PyMOL sessions."""
    
    def __init__(self, pymol_path: str = None):
        self.pymol_path = pymol_path or os.getenv("PYMOL_PATH", "pymol")
        self.session_active = False
        self.current_session = None
    
    def execute_command(self, command: str) -> Dict[str, Any]:
        """Execute a PyMOL command and return the result."""
        try:
            # Create PyMOL script
            script_content = f"""
import sys
try:
    {command}
    print("SUCCESS: Command executed")
except Exception as e:
    print(f"ERROR: {{e}}")
    sys.exit(1)
"""
            
            # Write to temporary script file
            script_file = Path("/tmp/pymol_script.py")
            script_file.write_text(script_content)
            
            # Execute PyMOL with the script
            result = subprocess.run(
                [self.pymol_path, "-cq", str(script_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Clean up
            script_file.unlink(missing_ok=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "output": result.stdout,
                    "command": command
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr,
                    "command": command
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timed out after 30 seconds",
                "command": command
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": command
            }
    
    def load_structure(self, file_path: str) -> Dict[str, Any]:
        """Load a molecular structure file in PyMOL."""
        if not Path(file_path).exists():
            return {
                "success": False,
                "error": f"File not found: {file_path}"
            }
        
        command = f'load "{file_path}"'
        return self.execute_command(command)
    
    def get_object_list(self) -> Dict[str, Any]:
        """Get list of objects currently loaded in PyMOL."""
        command = "print(cmd.get_object_list())"
        return self.execute_command(command)
    
    def set_representation(self, object_name: str, representation: str) -> Dict[str, Any]:
        """Set molecular representation for an object."""
        valid_reps = ["lines", "sticks", "spheres", "surface", "cartoon", "ribbon"]
        if representation.lower() not in valid_reps:
            return {
                "success": False,
                "error": f"Invalid representation. Valid options: {valid_reps}"
            }
        
        command = f'show {representation}, {object_name}'
        return self.execute_command(command)
    
    def color_object(self, object_name: str, color: str) -> Dict[str, Any]:
        """Apply color to a molecular object."""
        command = f'color {color}, {object_name}'
        return self.execute_command(command)
    
    def zoom_object(self, object_name: str) -> Dict[str, Any]:
        """Zoom to a specific object."""
        command = f'zoom {object_name}'
        return self.execute_command(command)
    
    def save_image(self, filename: str, width: int = 800, height: int = 600) -> Dict[str, Any]:
        """Save current PyMOL view as an image."""
        command = f'png {filename}, {width}, {height}'
        return self.execute_command(command)
    
    def get_selection_info(self, selection: str = "all") -> Dict[str, Any]:
        """Get information about a selection."""
        command = f'''
print(f"Number of atoms: {{cmd.count_atoms()}}")
print(f"Number of bonds: {{cmd.count_bonds()}}")
print(f"Center of mass: {{cmd.get_center_of_mass()}}")
'''
        return self.execute_command(command)


# PyMOL tool functions for the agent
def execute_pymol_command(command: str) -> dict:
    """Execute a PyMOL command and return the result.
    
    Args:
        command: The PyMOL command to execute
        
    Returns:
        Dictionary containing success status and result/error message
    """
    executor = PyMOLCommandExecutor()
    return executor.execute_command(command)


def load_molecule(file_path: str) -> dict:
    """Load a molecular structure file in PyMOL.
    
    Args:
        file_path: Path to the molecular structure file (PDB, MOL2, etc.)
        
    Returns:
        Dictionary containing success status and result/error message
    """
    executor = PyMOLCommandExecutor()
    return executor.load_structure(file_path)


def set_molecular_representation(object_name: str, representation: str) -> dict:
    """Set the molecular representation for a loaded object.
    
    Args:
        object_name: Name of the object in PyMOL
        representation: Type of representation (lines, sticks, spheres, surface, cartoon, ribbon)
        
    Returns:
        Dictionary containing success status and result/error message
    """
    executor = PyMOLCommandExecutor()
    return executor.set_representation(object_name, representation)


def color_molecule(object_name: str, color: str) -> dict:
    """Apply color to a molecular object.
    
    Args:
        object_name: Name of the object in PyMOL
        color: Color name or RGB values
        
    Returns:
        Dictionary containing success status and result/error message
    """
    executor = PyMOLCommandExecutor()
    return executor.color_object(object_name, color)


def zoom_to_object(object_name: str) -> dict:
    """Zoom the camera to focus on a specific object.
    
    Args:
        object_name: Name of the object to zoom to
        
    Returns:
        Dictionary containing success status and result/error message
    """
    executor = PyMOLCommandExecutor()
    return executor.zoom_object(object_name)


def save_view_image(filename: str, width: int = 800, height: int = 600) -> dict:
    """Save the current PyMOL view as an image file.
    
    Args:
        filename: Name of the output image file
        width: Image width in pixels
        height: Image height in pixels
        
    Returns:
        Dictionary containing success status and result/error message
    """
    executor = PyMOLCommandExecutor()
    return executor.save_image(filename, width, height)


def get_molecule_info(selection: str = "all") -> dict:
    """Get information about molecules and selections.
    
    Args:
        selection: PyMOL selection string (default: "all")
        
    Returns:
        Dictionary containing molecular information
    """
    executor = PyMOLCommandExecutor()
    return executor.get_selection_info(selection)


def list_loaded_objects() -> dict:
    """List all objects currently loaded in PyMOL.
    
    Returns:
        Dictionary containing list of loaded objects
    """
    executor = PyMOLCommandExecutor()
    return executor.get_object_list()


# Utility function to register all PyMOL tools with the agent
def register_pymol_tools(agent):
    """Register all PyMOL tools with the agent."""
    pymol_tools = [
        ("execute_pymol_command", execute_pymol_command, 
         "Execute any PyMOL command and return the result"),
        ("load_molecule", load_molecule, 
         "Load a molecular structure file (PDB, MOL2, etc.) in PyMOL"),
        ("set_molecular_representation", set_molecular_representation, 
         "Set molecular representation (lines, sticks, spheres, surface, cartoon, ribbon)"),
        ("color_molecule", color_molecule, 
         "Apply color to a molecular object"),
        ("zoom_to_object", zoom_to_object, 
         "Zoom camera to focus on a specific object"),
        ("save_view_image", save_view_image, 
         "Save current PyMOL view as an image file"),
        ("get_molecule_info", get_molecule_info, 
         "Get information about molecules and selections"),
        ("list_loaded_objects", list_loaded_objects, 
         "List all objects currently loaded in PyMOL")
    ]
    
    for name, func, desc in pymol_tools:
        agent.add_tool(name, func, desc)