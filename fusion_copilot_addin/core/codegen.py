"""
Code Generation - Prompt templates and code assembly
"""

import json
from typing import Dict, Any, List


class CodeGenerator:
    """
    Assembles prompts and formats code generation results.
    
    Responsibilities:
    - Build system prompts with Fusion context
    - Format LLM responses into structured output
    - Generate patch/diff format for code modifications
    """
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    def build_prompt(self, user_message: str, fusion_context: Dict[str, Any]) -> str:
        """
        Build the complete prompt to send to LLM.
        
        Includes:
        - System instructions (Copilot-like behavior)
        - Current Fusion context
        - User request
        """
        
        system_prompt = self._get_system_prompt()
        context_summary = self._format_context(fusion_context)
        
        prompt = f"""{system_prompt}

## Current Fusion 360 Context:
{context_summary}

## User Request:
{user_message}

## Expected Output Format:
Provide response as JSON with the following structure:
{{
  "title": "Brief task name",
  "plan": ["Step 1", "Step 2", "Step 3"],
  "code": "Fusion 360 Python API code",
  "notes": "Assumptions and variations"
}}
"""
        return prompt
    
    def _get_system_prompt(self) -> str:
        """Get base system prompt for Copilot-like behavior"""
        return """You are an expert Fusion 360 Python API assistant. Your role is to:

1. Generate runnable Fusion 360 Python code based on user requests
2. Use best practices: modular functions, proper error handling, named features
3. Prefer parametric design: use user parameters for dimensions
4. Be idempotent when reasonable (avoid duplicating features)
5. Include helpful comments in code
6. Suggest only valid Fusion 360 API calls

When the user requests part generation, CAM setup, or drawing creation:
- Create parametric designs with user-defined parameters
- Use proper feature naming for later edits
- Include necessary sketches, extrudes, holes, patterns, fillets
- Add safety checks for null/empty objects

When the user requests edits to existing geometry:
- Read existing parameters and feature names
- Update values or edit features safely
- Preserve other geometry unchanged"""
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context dict into readable text for the prompt"""
        lines = []
        
        if context.get('document'):
            doc = context['document']
            lines.append(f"Document: {doc.get('name', 'Unknown')}")
            lines.append(f"Units: {context.get('units', 'mm')}")
        
        if context.get('parameters'):
            lines.append(f"User Parameters: {len(context['parameters'])} defined")
            for param in context['parameters'][:5]:  # Show first 5
                lines.append(f"  - {param.get('name')}: {param.get('value')}")
        
        if context.get('selection'):
            sel = context['selection']
            if sel.get('count', 0) > 0:
                lines.append(f"Selection: {sel['count']} entities selected")
        
        if context.get('components'):
            lines.append(f"Components: {len(context['components'])} top-level components")
        
        return "\n".join(lines) if lines else "No context available"
    
    def parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse LLM response and extract code, plan, title, notes.
        
        Handles multiple formats:
        - JSON format (preferred)
        - Markdown code blocks
        - Plain text responses
        """
        try:
            # Try parsing as JSON first
            result = json.loads(response_text)
            return {
                "title": result.get("title", "Generated Code"),
                "plan": result.get("plan", []),
                "code": result.get("code", ""),
                "notes": result.get("notes", ""),
            }
        except json.JSONDecodeError:
            # Fall back to markdown parsing
            return self._parse_markdown_response(response_text)
    
    def _parse_markdown_response(self, text: str) -> Dict[str, Any]:
        """Parse markdown-formatted response"""
        lines = text.split('\n')
        code_block = []
        plan = []
        title = "Generated Code"
        notes = ""
        in_code = False
        
        for line in lines:
            if line.startswith('```python') or line.startswith('```'):
                in_code = not in_code
            elif in_code:
                code_block.append(line)
            elif line.startswith('# '):
                title = line[2:].strip()
            elif line.startswith('- '):
                plan.append(line[2:].strip())
        
        return {
            "title": title,
            "plan": plan,
            "code": '\n'.join(code_block),
            "notes": notes,
        }


class PatchGenerator:
    """
    Generate unified diff patches for code modifications.
    """
    
    @staticmethod
    def generate_patch(original_code: str, modified_code: str) -> str:
        """Generate a unified diff patch"""
        # TODO: Implement diff generation
        return ""
    
    @staticmethod
    def apply_patch(original_code: str, patch: str) -> str:
        """Apply a patch to code"""
        # TODO: Implement patch application
        return ""
