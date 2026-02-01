# Fusion 360 Copilot Assistant - Directory Structure

```
fusion_copilot_addin/
│
├── 📄 manifest.json                    Fusion add-in configuration
├── 📄 main.py                          Add-in entry point
├── 📄 config.py                        Configuration and settings
│
├── 📁 core/                            Core orchestration
│   ├── __init__.py
│   ├── orchestrator.py                 Request router and coordinator
│   ├── context.py                      Live Fusion context capture
│   ├── executor.py                     Safe code execution + diagnostics
│   └── codegen.py                      Prompt building and response parsing
│
├── 📁 tools/                           Integration utilities
│   ├── __init__.py
│   ├── filesystem.py                   Project scanning, tool libraries
│   ├── geometry_extract.py             Mesh/geometry metadata extraction
│   └── vision_extract.py               OCR, blueprint analysis
│
├── 📁 ui/                              User interface
│   ├── panel.html                      Chat panel markup
│   ├── panel.css                       Styling (light/dark theme)
│   └── panel.js                        Client-side logic
│
├── 📁 scripts/                         Utilities and examples
│   ├── __init__.py
│   ├── sandbox_runner.py               Isolated execution utilities
│   └── examples.py                     Example scripts (parametric parts, CAM)
│
├── 📄 README.md                        Full documentation
├── 📄 REQUIREMENTS.md                  Dependencies and setup
├── 📄 ARCHITECTURE.md                  (this file) Structure overview
│
```

## File Descriptions

### Configuration Files
- **manifest.json**: Fusion 360 add-in manifest - tells Fusion how to load the add-in
- **config.py**: Central configuration - LLM backends, UI settings, feature flags
- **REQUIREMENTS.md**: Python and system dependencies

### Entry Point
- **main.py**: Initializes the add-in when Fusion starts, sets up UI and command handlers

### Core Modules

#### orchestrator.py
Coordinates the entire flow:
- Receives chat messages from UI
- Calls context capture
- Sends requests to LLM
- Routes code to executor
- Handles results/errors

#### context.py
Captures live Fusion 360 state for AI prompts:
- Document name, file path, units
- Selected entities (faces, edges, bodies)
- User parameters and their values
- Component structure
- CAM context (if in CAM workspace)
- Returns structured JSON

#### executor.py
Safely runs generated Fusion API code:
- Transaction management (begin/commit)
- Output/error capture
- Stack trace formatting
- Error diagnosis (common patterns)
- Suggests fixes for common mistakes

#### codegen.py
Code generation infrastructure:
- Builds system prompts with context
- Parses LLM responses (JSON, Markdown)
- Extracts title, plan, code, notes
- Generates patch diffs for modifications

### Tools Module

#### filesystem.py
Project directory integration:
- Scans for geometry files (STEP, STL, IGES, OBJ)
- Reads project documentation
- Loads tool libraries (JSON)
- Read-only access by default

#### geometry_extract.py
Geometry metadata extraction:
- Bounding boxes
- Face/edge counts
- Feature detection (holes, pockets)
- Mesh information

#### vision_extract.py
Image and PDF analysis:
- OCR text extraction from blueprints
- Dimension detection
- PDF specification extraction

### UI Module

#### panel.html
Chat interface structure:
- Message history
- User input area
- Code preview panel
- Execution/error displays
- Settings modal

#### panel.css
Professional styling:
- Light and dark themes
- Responsive layout
- Syntax highlighting for code
- Loading animations
- Error/success indicators

#### panel.js
Client-side logic:
- Message sending/display
- Code panel control
- Settings persistence
- Event handling
- Mock LLM responses (replaced with real backend)

### Scripts Module

#### sandbox_runner.py
Isolated code execution utilities:
- Captures stdout/stderr
- Exception handling
- Execution timing
- Safe globals scope

#### examples.py
Reference implementations:
- Parametric bracket generation
- CAM setup creation
- Drawing generation
- Best practices examples

## Data Flow

```
User Input (Chat)
    ↓
[panel.js sends message]
    ↓
orchestrator.process_chat_message()
    ↓
context_capture.get_runtime_context()  ← Reads live Fusion state
    ↓
[Build prompt with context]
    ↓
[Call LLM (OpenAI/Ollama/Offline)]
    ↓
codegen.parse_llm_response()
    ↓
[Show code panel with plan, code, notes]
    ↓
User clicks "Apply"
    ↓
executor.run_code()
    ↓
[Execute in Fusion transaction]
    ↓
[Show result or error]
    ↓
[User can Undo via Fusion]
```

## Extension Points

### Adding a New LLM Backend
1. Create `llm_backends/my_backend.py`
2. Implement `LLMBackend` interface
3. Update `config.py` to register backend
4. UI automatically supports it

### Adding Custom Tools
1. Create `tools/my_tool.py`
2. Implement tool interface
3. Register in `orchestrator.py`
4. Include in context prompts

### Custom Workflows
1. Add workflow class to `core/workflows.py`
2. Register in `orchestrator.py`
3. UI routing handles it

## Naming Conventions

- `_private_method()` - Internal functions
- `PUBLIC_CONSTANT` - Configuration constants
- `snake_case` - Python variables/functions
- `camelCase` - JavaScript variables
- `PascalCase` - Python classes, JS classes

## Error Handling Strategy

1. **User-facing errors**: Clear messages + suggestions
2. **API errors**: Diagnose and offer fixes
3. **Network errors**: Fallback to offline mode
4. **State errors**: Validate Fusion state before execution

## Testing Strategy

- Unit tests for core modules
- Integration tests for orchestrator
- Mock Fusion API for offline testing
- E2E tests with actual Fusion if available

## Performance Considerations

- Context capture: ~100-500ms per request
- LLM inference: 2-30s depending on backend
- Code execution: 100ms - 5s depending on operation
- UI responsiveness: Never block on LLM calls (async)

---

**Current Status**: Phase 1 Infrastructure Complete ✓
