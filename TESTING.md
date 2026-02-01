# How to Run Tests

## Quick Start

You can test the application using the RUN test suite:

### From Command Prompt (cmd.exe)
```bash
RUN.bat
```

### From PowerShell
```powershell
.\RUN.ps1
```

### What Gets Tested

The RUN test suite validates:

1. **Project Structure** (5/5)
   - All required directories exist
   - All core files are present

2. **Python Syntax** (14/14)
   - All 14 Python files compile without errors
   - Requires: Python 3.8+ installed

3. **Configuration Validation** (1/1)
   - manifest.json is valid JSON
   - Correct add-in ID configured

4. **Web Assets** (3/3)
   - panel.html has valid HTML structure
   - panel.css contains required CSS rules
   - panel.js contains required JavaScript functions

5. **Documentation** (3/3)
   - README.md, ARCHITECTURE.md, REQUIREMENTS.md exist
   - All documentation files have content

6. **Core Modules** (4/4)
   - orchestrator.py: Orchestrator class and process_chat_message method
   - context.py: ContextCapture class and get_runtime_context method
   - executor.py: CodeExecutor class and run_code method
   - codegen.py: CodeGenerator class and build_prompt method

## Test Results

```
[PASS] 42 tests
[FAIL] 0 tests
Total: 42

Status: OK - ALL TESTS PASSED - READY TO COMMIT
Exit Code: 0 (success)
```

## Before Committing

Always run the test suite to ensure:
- ✓ No Python syntax errors
- ✓ All required files are present
- ✓ Configuration is valid
- ✓ Documentation is complete
- ✓ Core modules have required components

## Common Issues

### Python Not Found
If you see "Python not found - skipping syntax check":
- Install Python 3.8+ from https://www.python.org
- Add Python to PATH

### Execution Policy Error
If running from PowerShell directly fails:
- Use: `powershell -ExecutionPolicy Bypass -File .\RUN.ps1`
- Or use: `.\RUN.bat` (batch file handles this automatically)

## What Changed

The test runner validates:
- File existence and structure
- Python code correctness
- Configuration integrity
- Required components in each module
- Documentation completeness

This helps catch issues before committing to git.
