# Fusion 360 Copilot-Style Assistant

An AI-powered Copilot-like assistant for Autodesk Fusion 360 that generates parametric parts, CAM setups, and drawings using natural language.

## Features

### 🤖 Core Capabilities
- **Chat-based Code Generation**: Describe what you want, get Fusion 360 Python code
- **Inline Copilot Mode**: Code completions while editing scripts
- **Context Awareness**: AI understands your current document, selection, and parameters
- **Safe Execution**: Code runs in controlled transactions with automatic undo
- **Error Recovery**: Smart diagnostics and auto-fix suggestions

### 📋 Supported Workflows
- **Parametric Part Generation**: Create designs with user-defined parameters
- **Geometry Editing**: Modify existing features intelligently
- **CAM Setup Creation**: Generate milling operations and toolpaths
- **Drawing Generation**: Create technical drawings with automatic callouts
- **Project Integration**: Reference local files (STEP, STL, images, PDFs)

## Architecture

```
fusion_copilot_addin/
├── manifest.json              # Fusion add-in manifest
├── main.py                    # Entry point
├── core/
│   ├── orchestrator.py        # Routes requests between UI and executor
│   ├── context.py             # Captures live Fusion context
│   ├── executor.py            # Safely executes generated code
│   └── codegen.py             # Prompt building and code parsing
├── tools/
│   ├── filesystem.py          # Project file scanning
│   ├── geometry_extract.py    # Geometry metadata extraction
│   └── vision_extract.py      # OCR and image analysis
├── scripts/
│   ├── sandbox_runner.py      # Isolated code execution
│   └── examples.py            # Example scripts
└── ui/
    ├── panel.html             # Chat UI
    ├── panel.css              # Styling
    └── panel.js               # Client-side logic
```

## Key Components

### Orchestrator (`core/orchestrator.py`)
- Central hub receiving chat messages from the UI
- Enriches requests with current Fusion context
- Routes to LLM for code generation
- Coordinates code execution and error handling

### Context Capture (`core/context.py`)
- Captures live Fusion 360 state:
  - Active document, units, workspace
  - User parameters and components
  - Selected entities
  - CAM setups/operations (if in CAM workspace)
- Returns structured JSON for LLM prompts

### Code Executor (`core/executor.py`)
- Executes generated code in Fusion API context
- Transaction management for safe undo
- Captures output and exceptions
- Error diagnostics and fix suggestions

### Code Generator (`core/codegen.py`)
- Builds system prompts with context
- Parses LLM responses (JSON, Markdown)
- Generates patch diffs for code modifications
- Formats output for UI display

## UX Flows

### Chat Mode
```
User: "Create a parametric bracket with width/height/thickness"
  ↓
[Capture context]
  ↓
[Send to LLM with system prompt]
  ↓
AI: Shows plan, code, and notes
  ↓
User: Reviews → "Apply"
  ↓
[Execute in transaction]
  ↓
Result: "✓ Created 3 user parameters..."
```

### Inline Mode
```
User: Editing a script, types: "# ai: add a hole pattern"
  ↓
[Context from selection + document]
  ↓
AI: Suggests code completion inline
  ↓
User: Tab to accept, or Escape to reject
```

## LLM Integration

### Supported Models
- OpenAI GPT-4 (cloud)
- Local LLM via Ollama (offline-capable)
- Offline mode (code templates only)

### System Prompt
The assistant includes:
1. **Role Definition**: "Expert Fusion 360 Python API assistant"
2. **Requirements**:
   - Modular, well-commented code
   - Fusion best practices
   - Parametric design preference
   - Idempotent operations when reasonable
3. **Context**: Current doc, parameters, selection, components

## Error Handling

When code execution fails:
1. **Diagnosis**: Analyzes error type (AttributeError, TypeError, etc.)
2. **Suggestions**: Offers common fixes
3. **Auto-Fix**: (Optional) LLM generates corrected code
4. **Fallback**: User can edit code manually or ask for clarification

Example:
```
Error: AttributeError: 'NoneType' object has no attribute 'sketchCurves'

Suggestions:
- Check that the component is not null before accessing
- Add null checks: if obj is not None:
- Ensure design workspace is active
```

## Safety Features

- **No Silent Writes**: All file operations require explicit user confirmation
- **Reversible Changes**: All modifications use Fusion's undo stack
- **Named Features**: AI always names created features for traceability
- **Read-Only by Default**: Project file scanner reads-only unless explicitly requested
- **Transaction Boundaries**: Code runs in controlled scopes with rollback support

## Configuration

Settings stored in `localStorage`:
```json
{
    "model": "openai",
    "apiKey": "sk-...",
    "projectRoot": "C:/My Project/",
    "autoRun": false
}
```

Optional `project.copilot.json` in project root:
```json
{
    "modelBackend": "openai",
    "toolLibrary": "tools/tools.json",
    "excludeDirs": ["bin", "obj", "cache"],
    "maxContextSize": 8000
}
```

## Development Status

### Phase 1 (Infrastructure) ✓ COMPLETE
- ✓ Add-in structure and manifest
- ✓ Core modules (orchestrator, context, executor)
- ✓ Chat UI (HTML, CSS, JavaScript)
- ✓ Code generation framework
- ✓ Error handling structure

### Phase 2 (LLM Integration) — IN PROGRESS
- [ ] OpenAI API integration
- [ ] Ollama local model support
- [ ] Prompt optimization
- [ ] Response parsing refinement

### Phase 3 (Advanced Features) — PLANNED
- [ ] Inline completions in script editor
- [ ] CAM operation generation
- [ ] Drawing creation
- [ ] Geometry analysis and feature detection
- [ ] Vision-based design import (OCR, blueprints)

## Installation

1. Clone this repository to your Fusion add-ins folder:
   ```
   C:\Users\[User]\AppData\Roaming\Autodesk\Fusion 360\API\addins\
   ```

2. Rename folder to `Assist360` (must match manifest ID)

3. Restart Fusion 360

4. The "Copilot Assistant" palette appears in the UI

## Usage

1. **Open a design** or create a new document
2. **Click the Copilot palette** (right panel)
3. **Describe your design**: "Create a 100mm x 50mm parametric bracket"
4. **Review the generated code** and plan
5. **Click "Apply"** to execute
6. **Use Fusion Undo** if you need to revert

## API Reference

### `Orchestrator.process_chat_message(user_message)`
Processes a user chat message and returns generated code.

**Returns:**
```python
{
    "title": "Parametric Bracket",
    "plan": ["Step 1", "Step 2", ...],
    "code": "# Python code here",
    "notes": "Assumptions and variations",
    "error": None  # If error occurred
}
```

### `ContextCapture.get_runtime_context()`
Captures current Fusion state.

**Returns:**
```python
{
    "document": {"name": "...", "file_path": "..."},
    "selection": {"count": 2, "entities": [...]},
    "parameters": [{"name": "Width", "value": "100", "unit": "mm"}],
    "components": [{"name": "Bracket", "occurrence_count": 1}],
    "units": "mm",
    "workspace": "Design",
    "cam": None
}
```

### `CodeExecutor.run_code(code)`
Safely executes code in Fusion.

**Returns:**
```python
{
    "success": True,
    "output": "Execution output",
    "error": None,
    "stack_trace": None
}
```

## Roadmap

- [ ] **v0.2**: Full LLM integration
- [ ] **v0.3**: Inline copilot completions
- [ ] **v0.4**: CAM and drawing generation
- [ ] **v1.0**: Production-ready release

## Contributing

Contributions welcome! Areas of interest:
- LLM integration and prompt optimization
- Geometry analysis and feature detection
- CAM operation generation
- Testing and error cases

## License

MIT

## Support

- 📖 [Fusion 360 API Documentation](https://fusion360.autodesk.com/api/intro/)
- 💬 [GitHub Issues](https://github.com/assist360/fusion-copilot/issues)
- 📧 support@assist360.com
