"""
Filesystem Tools - Read project files and geometry metadata
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Any


class ProjectFileScanner:
    """
    Scans project directory for relevant files:
    - Geometry files (STL, STEP, IGES, OBJ)
    - Documentation (TXT, MD, PDF)
    - Tool libraries (JSON)
    - Images/blueprints (PNG, JPG)
    """
    
    GEOMETRY_EXTENSIONS = {'.stl', '.step', '.stp', '.iges', '.igs', '.obj'}
    DOC_EXTENSIONS = {'.txt', '.md', '.json', '.pdf'}
    IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.bmp'}
    
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root) if project_root else None
    
    def scan_project(self) -> Dict[str, List[str]]:
        """
        Scan project directory and categorize files.
        
        Returns:
            {
                "geometry_files": [...],
                "documentation": [...],
                "images": [...],
                "tool_libraries": [...],
            }
        """
        if not self.project_root or not self.project_root.exists():
            return {
                "geometry_files": [],
                "documentation": [],
                "images": [],
                "tool_libraries": [],
            }
        
        result = {
            "geometry_files": [],
            "documentation": [],
            "images": [],
            "tool_libraries": [],
        }
        
        for file_path in self.project_root.rglob('*'):
            if not file_path.is_file():
                continue
            
            suffix = file_path.suffix.lower()
            relative_path = str(file_path.relative_to(self.project_root))
            
            if suffix in self.GEOMETRY_EXTENSIONS:
                result["geometry_files"].append(relative_path)
            elif suffix in self.IMAGE_EXTENSIONS:
                result["images"].append(relative_path)
            elif suffix == '.json':
                result["tool_libraries"].append(relative_path)
            elif suffix in {'.txt', '.md', '.pdf'}:
                result["documentation"].append(relative_path)
        
        return result
    
    def read_file_content(self, file_path: str, max_lines: int = 100) -> Optional[str]:
        """
        Read text file content (with line limit for large files).
        
        Args:
            file_path: Relative path from project root
            max_lines: Maximum lines to read
        
        Returns:
            File content or None if not readable
        """
        if not self.project_root:
            return None
        
        full_path = self.project_root / file_path
        
        if not full_path.exists() or not full_path.is_file():
            return None
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        lines.append("... (file truncated)")
                        break
                    lines.append(line.rstrip())
                return '\n'.join(lines)
        except Exception:
            return None


class GeometryMetadataExtractor:
    """
    Extract structured metadata from geometry files:
    - Bounding box
    - File size
    - Face/edge count (from STL/STEP)
    - Hole patterns / feature locations
    """
    
    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from a geometry file.
        
        Returns basic metadata dict with file info and available geometry data.
        """
        path = Path(file_path)
        
        if not path.exists():
            return {"error": "File not found"}
        
        metadata = {
            "file_name": path.name,
            "file_size_mb": path.stat().st_size / (1024 * 1024),
            "extension": path.suffix.lower(),
        }
        
        # TODO: Implement geometry-specific parsing for STL, STEP, etc.
        # This would require additional libraries like trimesh, pyassimp, etc.
        
        return metadata


class ToolLibraryLoader:
    """
    Load tool definitions from JSON files for CAM operations.
    
    Expects format:
    {
        "tools": [
            {
                "name": "End Mill 10mm",
                "type": "end_mill",
                "diameter": 10,
                "flutes": 2,
                "material": "HSS",
                ...
            }
        ]
    }
    """
    
    def load_tool_library(self, file_path: str) -> Optional[List[Dict]]:
        """Load tool definitions from JSON file"""
        try:
            import json
            with open(file_path, 'r') as f:
                data = json.load(f)
                return data.get('tools', [])
        except Exception:
            return None
