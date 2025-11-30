"""
Phase 2: Tool Development - Vision Analyzer Tool
This module provides vision analysis capabilities for molecular visualization.
"""

import base64
import io
from typing import Dict, Any, List, Optional
from pathlib import Path
import json

try:
    from PIL import Image
    from PIL import ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class VisionAnalyzer:
    """Analyzes molecular images and provides visual insights."""
    
    def __init__(self):
        self.supported_formats = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    
    def analyze_image(self, image_path: str) -> Dict[str, Any]:
        """Analyze a molecular image and extract features."""
        if not PIL_AVAILABLE:
            return {
                "success": False,
                "error": "PIL library not available. Install with: pip install Pillow"
            }
        
        if not Path(image_path).exists():
            return {
                "success": False,
                "error": f"Image file not found: {image_path}"
            }
        
        try:
            # Load and analyze image
            with Image.open(image_path) as img:
                # Basic image analysis
                width, height = img.size
                format_info = img.format
                mode = img.mode
                
                # Color analysis
                colors = self._analyze_colors(img)
                
                # Detect potential molecular features
                features = self._detect_molecular_features(img)
                
                return {
                    "success": True,
                    "image_info": {
                        "width": width,
                        "height": height,
                        "format": format_info,
                        "mode": mode
                    },
                    "color_analysis": colors,
                    "molecular_features": features,
                    "image_path": image_path
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error analyzing image: {str(e)}"
            }
    
    def _analyze_colors(self, img) -> Dict[str, Any]:
        """Analyze color distribution in the image."""
        try:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Get color histogram
            colors = img.getcolors(maxcolors=256*256*256)
            
            if colors:
                # Sort by frequency
                colors.sort(key=lambda x: x[0], reverse=True)
                
                # Get top colors
                top_colors = [(count, rgb) for count, rgb in colors[:10]]
                
                return {
                    "total_unique_colors": len(colors),
                    "dominant_colors": top_colors,
                    "analysis": "Color distribution calculated successfully"
                }
            else:
                return {"analysis": "Could not analyze colors"}
                
        except Exception as e:
            return {"error": f"Color analysis failed: {str(e)}"}
    
    def _detect_molecular_features(self, img) -> Dict[str, Any]:
        """Detect potential molecular visualization features."""
        features = {
            "spheres_detected": False,
            "sticks_detected": False,
            "surface_detected": False,
            "cartoon_detected": False,
            "labels_detected": False,
            "analysis": "Basic feature detection completed"
        }
        
        try:
            # Simple heuristic-based feature detection
            # This is a basic implementation - could be enhanced with ML models
            
            width, height = img.size
            pixels = list(img.getdata())
            
            # Convert to grayscale for analysis
            if img.mode != 'L':
                img_gray = img.convert('L')
                pixels = list(img_gray.getdata())
            
            # Edge detection heuristic
            edge_pixels = sum(1 for i in range(1, len(pixels)) 
                            if abs(pixels[i] - pixels[i-1]) > 30)
            edge_ratio = edge_pixels / len(pixels)
            
            # Feature heuristics (simplified)
            if edge_ratio > 0.15:
                features["surface_detected"] = True
            
            if edge_ratio > 0.05 and edge_ratio <= 0.15:
                features["cartoon_detected"] = True
            
            if edge_ratio > 0.2:
                features["sticks_detected"] = True
            
            # Check for distinct circular objects (spheres)
            # This would require more sophisticated image processing
            
            return features
            
        except Exception as e:
            features["error"] = f"Feature detection failed: {str(e)}"
            return features
    
    def annotate_image(self, image_path: str, annotations: List[Dict]) -> Dict[str, Any]:
        """Add annotations to an image."""
        if not PIL_AVAILABLE:
            return {
                "success": False,
                "error": "PIL library not available. Install with: pip install Pillow"
            }
        
        try:
            with Image.open(image_path) as img:
                draw = ImageDraw.Draw(img)
                
                for annotation in annotations:
                    x = annotation.get('x', 0)
                    y = annotation.get('y', 0)
                    text = annotation.get('text', '')
                    color = annotation.get('color', 'red')
                    
                    # Draw text annotation
                    draw.text((x, y), text, fill=color)
                
                # Save annotated image
                output_path = Path(image_path).stem + "_annotated" + Path(image_path).suffix
                img.save(output_path)
                
                return {
                    "success": True,
                    "annotated_image_path": output_path,
                    "annotations_added": len(annotations)
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error annotating image: {str(e)}"
            }
    
    def compare_images(self, image1_path: str, image2_path: str) -> Dict[str, Any]:
        """Compare two molecular images."""
        if not PIL_AVAILABLE:
            return {
                "success": False,
                "error": "PIL library not available. Install with: pip install Pillow"
            }
        
        try:
            with Image.open(image1_path) as img1, Image.open(image2_path) as img2:
                # Basic comparison
                size_same = img1.size == img2.size
                format_same = img1.mode == img2.mode
                
                # Simple pixel difference calculation
                if size_same and img1.mode == img2.mode:
                    if img1.mode != 'RGB':
                        img1 = img1.convert('RGB')
                        img2 = img2.convert('RGB')
                    
                    # Calculate differences
                    pixels1 = list(img1.getdata())
                    pixels2 = list(img2.getdata())
                    
                    total_diff = sum(abs(p1[i] - p2[i]) for p1, p2 in zip(pixels1, pixels2) for i in range(3))
                    avg_diff = total_diff / (len(pixels1) * 3)
                    
                    similarity = max(0, 100 - (avg_diff / 255 * 100))
                else:
                    similarity = "Cannot calculate - different sizes or formats"
                
                return {
                    "success": True,
                    "size_same": size_same,
                    "format_same": format_same,
                    "similarity_percentage": similarity,
                    "image1_info": {"size": img1.size, "mode": img1.mode},
                    "image2_info": {"size": img2.size, "mode": img2.mode}
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error comparing images: {str(e)}"
            }


# Vision tool functions for the agent
def analyze_molecular_image(image_path: str) -> dict:
    """Analyze a molecular image and extract visual features.
    
    Args:
        image_path: Path to the molecular image file
        
    Returns:
        Dictionary containing image analysis results
    """
    analyzer = VisionAnalyzer()
    return analyzer.analyze_image(image_path)


def annotate_molecular_image(image_path: str, annotations: list) -> dict:
    """Add annotations to a molecular image.
    
    Args:
        image_path: Path to the molecular image file
        annotations: List of annotation dictionaries with 'x', 'y', 'text', and 'color' keys
        
    Returns:
        Dictionary containing annotation results
    """
    analyzer = VisionAnalyzer()
    return analyzer.annotate_image(image_path, annotations)


def compare_molecular_images(image1_path: str, image2_path: str) -> dict:
    """Compare two molecular images for similarity.
    
    Args:
        image1_path: Path to the first image
        image2_path: Path to the second image
        
    Returns:
        Dictionary containing comparison results
    """
    analyzer = VisionAnalyzer()
    return analyzer.compare_images(image1_path, image2_path)


def get_image_info(image_path: str) -> dict:
    """Get basic information about an image file.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary containing image information
    """
    if not PIL_AVAILABLE:
        return {
            "success": False,
            "error": "PIL library not available. Install with: pip install Pillow"
        }
    
    try:
        with Image.open(image_path) as img:
            return {
                "success": True,
                "size": img.size,
                "format": img.format,
                "mode": img.mode,
                "file_size": Path(image_path).stat().st_size if Path(image_path).exists() else 0
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error reading image: {str(e)}"
        }


# Utility function to register all vision tools with the agent
def register_vision_tools(agent):
    """Register all vision analysis tools with the agent."""
    vision_tools = [
        ("analyze_molecular_image", analyze_molecular_image, 
         "Analyze a molecular image and extract visual features"),
        ("annotate_molecular_image", annotate_molecular_image, 
         "Add annotations to a molecular image"),
        ("compare_molecular_images", compare_molecular_images, 
         "Compare two molecular images for similarity"),
        ("get_image_info", get_image_info, 
         "Get basic information about an image file")
    ]
    
    for name, func, desc in vision_tools:
        agent.add_tool(name, func, desc)