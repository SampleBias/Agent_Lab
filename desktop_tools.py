"""
Phase 2: Tool Development - Desktop Controller Tool
This module provides desktop automation capabilities for GUI interaction.
"""

import subprocess
import time
import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

try:
    import pyautogui
    import pygetwindow as gw
    AUTOMATION_AVAILABLE = True
    # Configure pyautogui to be safer
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5
except ImportError:
    AUTOMATION_AVAILABLE = False


class DesktopController:
    """Controls desktop applications and GUI interactions."""
    
    def __init__(self):
        self.screen_size = None
        if AUTOMATION_AVAILABLE:
            self.screen_size = pyautogui.size()
    
    def get_screen_info(self) -> Dict[str, Any]:
        """Get screen dimensions and display information."""
        if not AUTOMATION_AVAILABLE:
            return {
                "success": False,
                "error": "Desktop automation libraries not available. Install with: pip install pyautogui pygetwindow"
            }
        
        return {
            "success": True,
            "screen_width": self.screen_size.width,
            "screen_height": self.screen_size.height,
            "current_position": pyautogui.position()
        }
    
    def find_window(self, title_pattern: str) -> Dict[str, Any]:
        """Find windows matching a title pattern."""
        if not AUTOMATION_AVAILABLE:
            return {
                "success": False,
                "error": "Desktop automation libraries not available"
            }
        
        try:
            windows = gw.getWindowsWithTitle(title_pattern)
            
            if not windows:
                # Try partial match
                    all_windows = gw.getAllWindows()
                    windows = [w for w in all_windows if title_pattern.lower() in w.title.lower()]
            
            if windows:
                window_list = []
                for window in windows:
                    window_list.append({
                        "title": window.title,
                        "left": window.left,
                        "top": window.top,
                        "width": window.width,
                        "height": window.height,
                        "is_active": window.isActive,
                        "is_visible": window.visible
                    })
                
                return {
                    "success": True,
                    "windows_found": len(windows),
                    "windows": window_list
                }
            else:
                return {
                    "success": False,
                    "error": f"No windows found matching pattern: {title_pattern}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error finding windows: {str(e)}"
            }
    
    def activate_window(self, title: str) -> Dict[str, Any]:
        """Activate and bring a window to the foreground."""
        if not AUTOMATION_AVAILABLE:
            return {
                "success": False,
                "error": "Desktop automation libraries not available"
            }
        
        try:
            windows = gw.getWindowsWithTitle(title)
            if not windows:
                windows = [w for w in gw.getAllWindows() if title.lower() in w.title.lower()]
            
            if windows:
                window = windows[0]
                window.activate()
                time.sleep(0.5)  # Wait for activation
                
                return {
                    "success": True,
                    "activated_window": {
                        "title": window.title,
                        "position": (window.left, window.top),
                        "size": (window.width, window.height)
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"Window not found: {title}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error activating window: {str(e)}"
            }
    
    def click_at_position(self, x: int, y: int, button: str = "left") -> Dict[str, Any]:
        """Click at specified screen coordinates."""
        if not AUTOMATION_AVAILABLE:
            return {
                "success": False,
                "error": "Desktop automation libraries not available"
            }
        
        try:
            if button == "left":
                pyautogui.click(x, y)
            elif button == "right":
                pyautogui.rightClick(x, y)
            elif button == "double":
                pyautogui.doubleClick(x, y)
            else:
                pyautogui.click(x, y, button=button)
            
            return {
                "success": True,
                "action": f"Clicked {button} button at ({x}, {y})"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error clicking at position: {str(e)}"
            }
    
    def type_text(self, text: str, interval: float = 0.1) -> Dict[str, Any]:
        """Type text using keyboard."""
        if not AUTOMATION_AVAILABLE:
            return {
                "success": False,
                "error": "Desktop automation libraries not available"
            }
        
        try:
            pyautogui.typewrite(text, interval=interval)
            return {
                "success": True,
                "action": f"Typed text: {text[:50]}{'...' if len(text) > 50 else ''}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error typing text: {str(e)}"
            }
    
    def press_key(self, key: str) -> Dict[str, Any]:
        """Press a keyboard key."""
        if not AUTOMATION_AVAILABLE:
            return {
                "success": False,
                "error": "Desktop automation libraries not available"
            }
        
        try:
            pyautogui.press(key)
            return {
                "success": True,
                "action": f"Pressed key: {key}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error pressing key: {str(e)}"
            }
    
    def take_screenshot(self, filename: str = None) -> Dict[str, Any]:
        """Take a screenshot of the entire screen."""
        if not AUTOMATION_AVAILABLE:
            return {
                "success": False,
                "error": "Desktop automation libraries not available"
            }
        
        try:
            if not filename:
                timestamp = int(time.time())
                filename = f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot(filename)
            
            return {
                "success": True,
                "filename": filename,
                "size": screenshot.size
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error taking screenshot: {str(e)}"
            }
    
    def get_mouse_position(self) -> Dict[str, Any]:
        """Get current mouse position."""
        if not AUTOMATION_AVAILABLE:
            return {
                "success": False,
                "error": "Desktop automation libraries not available"
            }
        
        pos = pyautogui.position()
        return {
            "success": True,
            "x": pos.x,
            "y": pos.y
        }
    
    def drag_mouse(self, start_x: int, start_y: int, end_x: int, end_y: int, 
                   duration: float = 1.0) -> Dict[str, Any]:
        """Drag mouse from start position to end position."""
        if not AUTOMATION_AVAILABLE:
            return {
                "success": False,
                "error": "Desktop automation libraries not available"
            }
        
        try:
            pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration, 
                          button='left', start=(start_x, start_y))
            return {
                "success": True,
                "action": f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error dragging mouse: {str(e)}"
            }


# Desktop control tool functions for the agent
def get_desktop_info() -> dict:
    """Get desktop screen information.
    
    Returns:
        Dictionary containing screen dimensions and current mouse position
    """
    controller = DesktopController()
    return controller.get_screen_info()


def find_application_window(title_pattern: str) -> dict:
    """Find application windows matching a title pattern.
    
    Args:
        title_pattern: Pattern to match in window titles
        
    Returns:
        Dictionary containing information about found windows
    """
    controller = DesktopController()
    return controller.find_window(title_pattern)


def activate_application_window(title: str) -> dict:
    """Activate and bring an application window to the foreground.
    
    Args:
        title: Title of the window to activate
        
    Returns:
        Dictionary containing activation result
    """
    controller = DesktopController()
    return controller.activate_window(title)


def click_at_coordinates(x: int, y: int, button: str = "left") -> dict:
    """Click at specified screen coordinates.
    
    Args:
        x: X coordinate
        y: Y coordinate
        button: Mouse button ("left", "right", "double")
        
    Returns:
        Dictionary containing click result
    """
    controller = DesktopController()
    return controller.click_at_position(x, y, button)


def type_keyboard_text(text: str, interval: float = 0.1) -> dict:
    """Type text using the keyboard.
    
    Args:
        text: Text to type
        interval: Interval between keystrokes in seconds
        
    Returns:
        Dictionary containing typing result
    """
    controller = DesktopController()
    return controller.type_text(text, interval)


def press_keyboard_key(key: str) -> dict:
    """Press a keyboard key.
    
    Args:
        key: Key to press (e.g., 'enter', 'escape', 'ctrl+c')
        
    Returns:
        Dictionary containing key press result
    """
    controller = DesktopController()
    return controller.press_key(key)


def capture_screenshot(filename: str = None) -> dict:
    """Take a screenshot of the entire screen.
    
    Args:
        filename: Optional filename for the screenshot
        
    Returns:
        Dictionary containing screenshot result
    """
    controller = DesktopController()
    return controller.take_screenshot(filename)


def get_current_mouse_position() -> dict:
    """Get the current mouse cursor position.
    
    Returns:
        Dictionary containing mouse coordinates
    """
    controller = DesktopController()
    return controller.get_mouse_position()


def drag_mouse_coordinates(start_x: int, start_y: int, end_x: int, end_y: int, 
                         duration: float = 1.0) -> dict:
    """Drag mouse from start position to end position.
    
    Args:
        start_x: Starting X coordinate
        start_y: Starting Y coordinate
        end_x: Ending X coordinate
        end_y: Ending Y coordinate
        duration: Duration of drag in seconds
        
    Returns:
        Dictionary containing drag result
    """
    controller = DesktopController()
    return controller.drag_mouse(start_x, start_y, end_x, end_y, duration)


# Utility function to register all desktop control tools with the agent
def register_desktop_tools(agent):
    """Register all desktop control tools with the agent."""
    desktop_tools = [
        ("get_desktop_info", get_desktop_info, 
         "Get desktop screen information and mouse position"),
        ("find_application_window", find_application_window, 
         "Find application windows matching a title pattern"),
        ("activate_application_window", activate_application_window, 
         "Activate and bring an application window to the foreground"),
        ("click_at_coordinates", click_at_coordinates, 
         "Click at specified screen coordinates"),
        ("type_keyboard_text", type_keyboard_text, 
         "Type text using the keyboard"),
        ("press_keyboard_key", press_keyboard_key, 
         "Press a keyboard key"),
        ("capture_screenshot", capture_screenshot, 
         "Take a screenshot of the entire screen"),
        ("get_current_mouse_position", get_current_mouse_position, 
         "Get the current mouse cursor position"),
        ("drag_mouse_coordinates", drag_mouse_coordinates, 
         "Drag mouse from start position to end position")
    ]
    
    for name, func, desc in desktop_tools:
        agent.add_tool(name, func, desc)