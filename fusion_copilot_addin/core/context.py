"""
Context Capture - Gathers live Fusion 360 context for AI prompting
"""

import json
from typing import Dict, Any, List, Optional


class ContextCapture:
    """
    Captures the current state of Fusion 360:
    - Active document
    - Selection
    - User parameters
    - Components
    - CAM context (if in CAM workspace)
    - Units
    """
    
    def __init__(self, app):
        self.app = app
        self.ui = app.userInterface
        
    def get_runtime_context(self) -> Dict[str, Any]:
        """
        Capture all relevant Fusion 360 context as a JSON-serializable dict.
        This gets included in prompts to the AI.
        """
        try:
            doc = self.app.activeDocument
            if not doc:
                return self._empty_context()
            
            context = {
                "document": self._capture_document(doc),
                "selection": self._capture_selection(),
                "parameters": self._capture_parameters(doc),
                "components": self._capture_components(doc),
                "cam": self._capture_cam_context(),
                "units": self._get_units(doc),
                "workspace": self._get_active_workspace(),
            }
            
            return context
            
        except Exception as e:
            return {
                "error": str(e),
                "document": None,
                "selection": None,
                "parameters": [],
                "components": [],
                "cam": None,
                "units": "mm",
                "workspace": None,
            }
    
    def _capture_document(self, doc) -> Dict[str, Any]:
        """Extract document information"""
        try:
            return {
                "name": doc.name,
                "file_path": doc.dataFile.parentFolder.path if doc.dataFile else "Unsaved",
                "is_saved": not doc.isModified,
                "root_component_name": doc.design.rootComponent.name if doc.design else None,
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _capture_selection(self) -> Dict[str, Any]:
        """Extract currently selected entities"""
        try:
            selection = self.ui.activeSelectionSet
            if not selection:
                return {"count": 0, "entities": []}
            
            entities = []
            for i in range(selection.count):
                entity = selection.item(i)
                entities.append({
                    "type": type(entity).__name__,
                    "index": i,
                })
            
            return {
                "count": selection.count,
                "entities": entities,
            }
        except Exception as e:
            return {"error": str(e), "count": 0}
    
    def _capture_parameters(self, doc) -> List[Dict[str, Any]]:
        """Extract user parameters"""
        try:
            if not doc.design:
                return []
            
            parameters = []
            user_params = doc.design.userParameters
            
            for i in range(user_params.count):
                param = user_params.item(i)
                parameters.append({
                    "name": param.name,
                    "value": str(param.value),
                    "unit": param.unit if hasattr(param, 'unit') else None,
                })
            
            return parameters
        except Exception as e:
            return [{"error": str(e)}]
    
    def _capture_components(self, doc) -> List[Dict[str, Any]]:
        """Extract top-level component structure"""
        try:
            if not doc.design:
                return []
            
            components = []
            root = doc.design.rootComponent
            
            if root.childComponents:
                for i in range(root.childComponents.count):
                    comp = root.childComponents.item(i)
                    components.append({
                        "name": comp.name,
                        "occurrence_count": comp.occurrences.count if hasattr(comp, 'occurrences') else 0,
                    })
            
            return components
        except Exception as e:
            return [{"error": str(e)}]
    
    def _capture_cam_context(self) -> Optional[Dict[str, Any]]:
        """Extract CAM workspace info if active"""
        try:
            # TODO: Implement CAM context capture if CAM workspace is active
            return None
        except Exception:
            return None
    
    def _get_units(self, doc) -> str:
        """Get active document units"""
        try:
            if doc.design and doc.design.unitsManager:
                return doc.design.unitsManager.defaultLengthUnits
            return "mm"
        except Exception:
            return "mm"
    
    def _get_active_workspace(self) -> str:
        """Get current workspace (Design, CAM, Drawing, etc.)"""
        try:
            # TODO: Determine active workspace
            return "Design"
        except Exception:
            return "Unknown"
    
    def _empty_context(self) -> Dict[str, Any]:
        """Return empty context when no document is open"""
        return {
            "document": None,
            "selection": {"count": 0, "entities": []},
            "parameters": [],
            "components": [],
            "cam": None,
            "units": "mm",
            "workspace": None,
            "error": "No active document",
        }
