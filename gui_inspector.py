"""
Phase 2: Tool Development - GUI Inspector Tool
This module provides GUI inspection and accessibility capabilities.
"""

import json
import subprocess
import time
from typing import Dict, Any, List, Optional
from pathlib import Path

try:
    import pygetwindow as gw
    import pyautogui
    AUTOMATION_AVAILABLE = True
except ImportError:
    AUTOMATION_AVAILABLE = False

try:
    # Try to import accessibility libraries (platform-specific)
    if Path("/proc/version").exists():
        # Linux - try AT-SPI
        try:
            import pyatspi
            ACCESSIBILITY_AVAILABLE = True
        except ImportError:
            ACCESSIBILITY_AVAILABLE = False
    else:
        # Windows/macOS - would use different libraries
        ACCESSIBILITY_AVAILABLE = False
except:
    ACCESSIBILITY_AVAILABLE = False


class GUIInspector:
    """Inspects GUI elements and provides accessibility information."""
    
    def __init__(self):
        self.current_window = None
        self.accessibility_enabled = ACCESSIBILITY_AVAILABLE
    
    def get_window_hierarchy(self, window_title: str = None) -> Dict[str, Any]:
        """Get the hierarchy of GUI elements in a window."""
        if not AUTOMATION_AVAILABLE:
            return {
                "success": False,
                "error": "GUI automation libraries not available. Install with: pip install pygetwindow pyautogui"
            }
        
        try:
            if window_title:
                windows = gw.getWindowsWithTitle(window_title)
                if not windows:
                    windows = [w for w in gw.getAllWindows() if window_title.lower() in w.title.lower()]
                
                if windows:
                    target_window = windows[0]
                else:
                    return {
                        "success": False,
                        "error": f"Window not found: {window_title}"
                    }
            else:
                target_window = gw.getActiveWindow()
            
            if not target_window:
                return {
                    "success": False,
                    "error": "No active window found"
                }
            
            # Basic window information
            window_info = {
                "title": target_window.title,
                "size": (target_window.width, target_window.height),
                "position": (target_window.left, target_window.top),
                "is_active": target_window.isActive,
                "is_visible": target_window.visible
            }
            
            # Try to get more detailed GUI information
            if self.accessibility_enabled:
                detailed_info = self._get_accessibility_info(target_window)
                window_info["accessibility_elements"] = detailed_info
            else:
                window_info["note"] = "Detailed accessibility information not available"
            
            return {
                "success": True,
                "window": window_info
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error inspecting window: {str(e)}"
            }
    
    def _get_accessibility_info(self, window) -> List[Dict[str, Any]]:
        """Get detailed accessibility information from window."""
        # This is a placeholder implementation
        # Real implementation would use platform-specific accessibility APIs
        elements = []
        
        try:
            # Example of what could be extracted with accessibility APIs
            # This would require platform-specific implementation
            
            # Simulate finding some common GUI elements
            common_elements = [
                {"type": "button", "label": "File", "position": (10, 10), "size": (50, 25)},
                {"type": "button", "label": "Edit", "position": (65, 10), "size": (50, 25)},
                {"type": "menu", "label": "File Menu", "position": (10, 35), "size": (200, 300)},
            ]
            
            # In a real implementation, you'd use:
            # - AT-SPI on Linux
            # - UI Automation on Windows
            # - Accessibility APIs on macOS
            
            elements.extend(common_elements)
            
        except Exception as e:
            print(f"Accessibility info error: {e}")
        
        return elements
    
    def find_clickable_elements(self, window_title: str = None) -> Dict[str, Any]:
        """Find clickable elements in a window."""
        window_info = self.get_window_hierarchy(window_title)
        
        if not window_info["success"]:
            return window_info
        
        elements = []
        accessibility_elements = window_info["window"].get("accessibility_elements", [])
        
        for elem in accessibility_elements:
            if elem.get("type") in ["button", "menu", "link", "checkbox", "radio"]:
                elements.append({
                    "type": elem["type"],
                    "label": elem.get("label", ""),
                    "position": elem.get("position"),
                    "size": elem.get("size"),
                    "action": "click"
                })
        
        return {
            "success": True,
            "clickable_elements": elements,
            "total_found": len(elements)
        }
    
    def get_element_at_position(self, x: int, y: int) -> Dict[str, Any]:
        """Get GUI element at specific screen coordinates."""
        if not AUTOMATION_AVAILABLE:
            return {
                "success": False,
                "error": "GUI automation libraries not available"
            }
        
        try:
            # Get active window
            active_window = gw.getActiveWindow()
            
            if not active_window:
                return {
                    "success": False,
                    "error": "No active window"
                }
            
            # Check if coordinates are within active window
            if (active_window.left <= x <= active_window.left + active_window.width and
                active_window.top <= y <= active_window.top + active_window.height):
                
                # Try to identify element at this position
                # This would require platform-specific implementation
                element_info = {
                    "position": (x, y),
                    "window": active_window.title,
                    "relative_position": (x - active_window.left, y - active_window.top),
                    "note": "Detailed element identification requires platform-specific APIs"
                }
                
                return {
                    "success": True,
                    "element": element_info
                }
            else:
                return {
                    "success": False,
                    "error": f"Position ({x}, {y}) is outside active window bounds"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error identifying element: {str(e)}"
            }
    
    def capture_window_state(self, window_title: str = None) -> Dict[str, Any]:
        """Capture the current state of a window."""
        window_info = self.get_window_hierarchy(window_title)
        
        if not window_info["success"]:
            return window_info
        
        # Add timestamp and state information
        window_info["window"]["capture_timestamp"] = time.time()
        window_info["window"]["screen_resolution"] = pyautogui.size() if AUTOMATION_AVAILABLE else "Unknown"
        
        return {
            "success": True,
            "window_state": window_info["window"]
        }
    
    def list_all_windows(self) -> Dict[str, Any]:
        """List all visible windows."""
        if not AUTOMATION_AVAILABLE:
            return {
                "success": False,
                "error": "GUI automation libraries not available"
            }
        
        try:
            all_windows = gw.getAllWindows()
            window_list = []
            
            for window in all_windows:
                if window.visible and window.title.strip():
                    window_list.append({
                        "title": window.title,
                        "position": (window.left, window.top),
                        "size": (window.width, window.height),
                        "is_active": window.isActive
                    })
            
            return {
                "success": True,
                "windows": window_list,
                "total_windows": len(window_list)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error listing windows: {str(e)}"
            }
    
    def get_window_screenshot(self, window_title: str = None) -> Dict[str, Any]:
        """Take a screenshot of a specific window."""
        if not AUTOMATION_AVAILABLE:
            return {
                "success": False,
                "error": "GUI automation libraries not available"
            }
        
        try:
            if window_title:
                windows = gw.getWindowsWithTitle(window_title)
                if not windows:
                    windows = [w for w in gw.getAllWindows() if window_title.lower() in w.title.lower()]
                
                if windows:
                    target_window = windows[0]
                else:
                    return {
                        "success": False,
                        "error": f"Window not found: {window_title}"
                    }
            else:
                target_window = gw.getActiveWindow()
            
            if not target_window:
                return {
                    "success": False,
                    "error": "No active window found"
                }
            
            # Activate window and take screenshot
            target_window.activate()
            time.sleep(0.5)
            
            # Screenshot the window area
            screenshot = pyautogui.screenshot(
                region=(target_window.left, target_window.top, 
                       target_window.width, target_window.height)
            )
            
            filename = f"window_screenshot_{int(time.time())}.png"
            screenshot.save(filename)
            
            return {
                "success": True,
                "filename": filename,
                "window_title": target_window.title,
                "size": (target_window.width, target_window.height)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error taking window screenshot: {str(e)}"
            }


# GUI inspector tool functions for the agent
def inspect_window_hierarchy(window_title: str = None) -> dict:
    """Get the hierarchy of GUI elements in a window.
    
    Args:
        window_title: Optional title of the window to inspect
        
    Returns:
        Dictionary containing window hierarchy information
    """
    inspector = GUIInspector()
    return inspector.get_window_hierarchy(window_title)


def find_clickable_elements(window_title: str = None) -> dict:
    """Find clickable elements in a window.
    
    Args:
        window_title: Optional title of the window to inspect
        
    Returns:
        Dictionary containing clickable elements information
    """
    inspector = GUIInspector()
    return inspector.find_clickable_elements(window_title)


def get_element_at_coordinates(x: int, y: int) -> dict:
    """Get GUI element at specific screen coordinates.
    
    Args:
        x: X coordinate
        y: Y coordinate
        
    Returns:
        Dictionary containing element information at the position
    """
    inspector = GUIInspector()
    return inspector.get_element_at_position(x, y)


def capture_window_state(window_title: str = None) -> dict:
    """Capture the current state of a window.
    
    Args:
        window_title: Optional title of the window to capture
        
    Returns:
        Dictionary containing window state information
    """
    inspector = GUIInspector()
    return inspector.capture_window_state(window_title)


def list_visible_windows() -> dict:
    """List all visible windows.
    
    Returns:
        Dictionary containing list of visible windows
    """
    inspector = GUIInspector()
    return inspector.list_all_windows()


def screenshot_window(window_title: str = None) -> dict:
    """Take a screenshot of a specific window.
    
    Args:
        window_title: Optional title of the window to screenshot
        
    Returns:
        Dictionary containing screenshot result
    """
    inspector = GUIInspector()
    return inspector.get_window_screenshot(window_title)


# Utility function to register all GUI inspector tools with the agent
def register_gui_inspector_tools(agent):
    """Register all GUI inspector tools with the agent."""
    gui_tools = [
        ("inspect_window_hierarchy", inspect_window_hierarchy, 
         "Get the hierarchy of GUI elements in a window"),
        ("find_clickable_elements", find_clickable_elements, 
         "Find clickable elements in a window"),
        ("get_element_at_coordinates", get_element_at_coordinates, 
         "Get GUI element at specific screen coordinates"),
        ("capture_window_state", capture_window_state, 
         "Capture the current state of a window"),
        ("list_visible_windows", list_visible_windows, 
         "List all visible windows"),
        ("screenshot_window", screenshot_window, 
         "Take a screenshot of a specific window")
    ]
    
    for name, func, desc in gui_tools:
        agent.add_tool(name, func, desc)