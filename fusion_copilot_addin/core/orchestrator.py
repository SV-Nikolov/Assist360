"""
Orchestrator - Routes requests between UI, LLM, and code executor
"""

import json
from typing import Dict, Any, Optional


class Orchestrator:
    """
    Central orchestrator that:
    - Receives requests from UI (chat panel)
    - Enriches with Fusion context
    - Calls LLM for code generation
    - Routes to executor
    - Returns results to UI
    """
    
    def __init__(self, app, context_capture, executor):
        self.app = app
        self.context_capture = context_capture
        self.executor = executor
        self.llm_client = None  # Will be initialized with model selection
        
    def process_chat_message(self, user_message: str) -> Dict[str, Any]:
        """
        Main entry point for chat messages from the UI panel.
        
        Returns:
            {
                "title": str,
                "plan": list[str],
                "code": str,
                "notes": str,
                "error": Optional[str]
            }
        """
        try:
            # Capture current Fusion context
            context = self.context_capture.get_runtime_context()
            
            # Generate code using LLM
            result = self._generate_code(user_message, context)
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "code": "",
                "plan": [],
                "title": "Error",
                "notes": "Failed to generate code"
            }
    
    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        Execute generated code in Fusion 360.
        
        Returns:
            {
                "success": bool,
                "output": str,
                "error": Optional[str],
                "stack_trace": Optional[str]
            }
        """
        return self.executor.run_code(code)
    
    def get_code_explanation(self, code: str) -> str:
        """Get AI explanation of what code does"""
        # TODO: Call LLM for explanation
        return "Code explanation will be implemented"
    
    def _generate_code(self, user_message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call LLM to generate code based on user message and context.
        
        This is where the "Copilot-like" magic happens - enriching the prompt
        with live Fusion context.
        """
        # TODO: Integrate with LLM (OpenAI, local model, etc.)
        return {
            "title": "Generated Code",
            "plan": ["Step 1", "Step 2", "Step 3"],
            "code": "# Generated code will appear here",
            "notes": "This is a placeholder",
            "error": None
        }


class CodeGenerationRequest:
    """Encapsulates a code generation request"""
    
    def __init__(self, user_message: str, fusion_context: Dict[str, Any]):
        self.user_message = user_message
        self.fusion_context = fusion_context
        self.generated_code = None
        self.plan = None
        self.error = None
