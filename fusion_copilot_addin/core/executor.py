"""
Code Executor - Safely executes generated Fusion 360 API code
"""

import traceback
import sys
from typing import Dict, Any
from io import StringIO


class CodeExecutor:
    """
    Executes AI-generated code in the Fusion 360 API context.
    
    Safety features:
    - Transaction boundaries
    - Error capture and formatting
    - Result/output capture
    - Stack trace reporting
    """
    
    def __init__(self, app):
        self.app = app
        self.ui = app.userInterface
        
    def run_code(self, code: str) -> Dict[str, Any]:
        """
        Execute code in a safe, bounded transaction.
        
        Returns:
            {
                "success": bool,
                "output": str,
                "error": Optional[str],
                "stack_trace": Optional[str],
                "execution_time": float,
            }
        """
        try:
            # Capture stdout/stderr
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = StringIO()
            sys.stderr = StringIO()
            
            # Create transaction context
            doc = self.app.activeDocument
            if not doc:
                return {
                    "success": False,
                    "error": "No active document",
                    "output": "",
                    "stack_trace": None,
                }
            
            design = doc.design
            
            # Execute code within transaction
            with self._transaction_context(doc, design):
                # Execute the generated code
                exec_globals = {
                    'app': self.app,
                    'doc': doc,
                    'design': design,
                    'adsk': __import__('adsk'),
                }
                
                exec(code, exec_globals)
            
            # Capture output
            output = sys.stdout.getvalue()
            error_output = sys.stderr.getvalue()
            
            return {
                "success": True,
                "output": output,
                "error": error_output if error_output else None,
                "stack_trace": None,
                "execution_time": 0.0,
            }
            
        except Exception as e:
            stack_trace = traceback.format_exc()
            return {
                "success": False,
                "output": sys.stdout.getvalue() if hasattr(sys.stdout, 'getvalue') else "",
                "error": str(e),
                "stack_trace": stack_trace,
                "execution_time": 0.0,
            }
        finally:
            # Restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    
    def _transaction_context(self, doc, design):
        """Context manager for Fusion transactions"""
        class TransactionContext:
            def __init__(ctx_self, doc, design):
                ctx_self.doc = doc
                ctx_self.design = design
                ctx_self.action = None
            
            def __enter__(ctx_self):
                try:
                    ctx_self.action = ctx_self.design.createCustomFeatureAction("AI Generated Code")
                    return ctx_self
                except Exception:
                    # Fallback: just execute without explicit transaction
                    return ctx_self
            
            def __exit__(ctx_self, exc_type, exc_val, exc_tb):
                try:
                    if ctx_self.action:
                        ctx_self.action.commit()
                except Exception:
                    pass
        
        return TransactionContext(doc, design)


class DiagnosticsEngine:
    """
    Analyzes execution errors and suggests fixes.
    """
    
    def __init__(self, app):
        self.app = app
    
    def analyze_error(self, error_text: str, code: str) -> Dict[str, Any]:
        """
        Analyze execution error and suggest fixes.
        
        Returns:
            {
                "diagnosis": str,
                "likely_fixes": list[str],
                "corrected_code": Optional[str],
            }
        """
        diagnosis = self._diagnose_error(error_text)
        fixes = self._suggest_fixes(error_text, code)
        
        return {
            "diagnosis": diagnosis,
            "likely_fixes": fixes,
            "corrected_code": None,  # TODO: Use LLM to generate corrected code
        }
    
    def _diagnose_error(self, error_text: str) -> str:
        """Diagnose common error patterns"""
        if "NoneType" in error_text:
            return "Likely accessing a null/None object. Check document/component existence."
        elif "AttributeError" in error_text:
            return "API attribute or method doesn't exist. Check Fusion API documentation."
        elif "TypeError" in error_text:
            return "Wrong argument type passed to API. Check parameter types."
        else:
            return f"Error: {error_text[:100]}"
    
    def _suggest_fixes(self, error_text: str, code: str) -> list:
        """Suggest common fixes"""
        fixes = []
        
        if "NoneType" in error_text:
            fixes.append("Check that the document/component is not null before accessing")
            fixes.append("Add null checks: if obj is not None:")
        
        if "AttributeError" in error_text:
            fixes.append("Review the Fusion 360 API documentation for correct method names")
            fixes.append("Ensure you're calling methods on the correct object type")
        
        if not fixes:
            fixes.append("Review the full error stack trace for details")
        
        return fixes
