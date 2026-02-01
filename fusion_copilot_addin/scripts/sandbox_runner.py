"""
Sandbox Runner - Utilities for isolated code execution
"""

import sys
from io import StringIO
from typing import Dict, Any, Tuple


class SandboxRunner:
    """
    Run code in an isolated sandbox environment.
    Captures output, exceptions, and execution time.
    """
    
    @staticmethod
    def run_isolated(code: str, globals_dict: Dict = None, timeout: float = 30.0) -> Dict[str, Any]:
        """
        Run code in isolated scope.
        
        Returns:
            {
                "success": bool,
                "output": str,
                "error": Optional[str],
                "execution_time": float,
            }
        """
        import time
        
        if globals_dict is None:
            globals_dict = {}
        
        # Capture output
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        
        start_time = time.time()
        error = None
        success = True
        
        try:
            exec(code, globals_dict)
        except Exception as e:
            success = False
            error = str(e)
        finally:
            output = sys.stdout.getvalue()
            error_output = sys.stderr.getvalue()
            
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            
            execution_time = time.time() - start_time
        
        return {
            "success": success,
            "output": output,
            "error": error or error_output,
            "execution_time": execution_time,
        }
