# Fusion 360 Copilot Assistant - Requirements

## Core Dependencies

### Fusion 360 API
- Fusion 360 (2020 or later)
- Fusion API SDK (included with Fusion 360)

### Python (3.8+)
- Python standard library only for core functionality
- Optional: numpy, scipy for advanced geometry analysis

## Optional LLM Backends

### OpenAI (Cloud)
```
openai >= 1.0.0
```

### Ollama (Local/Offline)
- Download from https://ollama.ai
- Recommended models:
  - `neural-chat` - 13B, good for coding
  - `codellama` - Code-specialized
  - `mistral` - 7B lightweight option

### Local LLM (Advanced)
```
llama-cpp-python >= 0.2.0  # For local .gguf models
```

## Optional Enhancement Libraries

### Geometry Analysis
```
trimesh >= 3.20.0          # STL/OBJ mesh analysis
pyassimp >= 5.1.0          # Multi-format geometry import
```

### PDF/Image Processing
```
pytesseract >= 0.3.0       # OCR for blueprints
pdf2image >= 1.16.0        # PDF to image conversion
Pillow >= 10.0.0           # Image processing
```

### Development
```
pytest >= 7.0.0
black >= 23.0.0
flake8 >= 6.0.0
mypy >= 1.0.0
```

## Installation

### Basic Setup (Core Only)
1. Install Fusion 360
2. No additional Python packages required

### With OpenAI Support
```bash
pip install openai
```

### With Ollama (Recommended for Offline)
1. Download Ollama: https://ollama.ai
2. Pull a model: `ollama pull neural-chat`
3. Leave Ollama running in background (http://localhost:11434)

### With All Features
```bash
pip install openai trimesh pytesseract pdf2image Pillow
```

## System Requirements

### Minimum
- CPU: 4 cores
- RAM: 8 GB (for Fusion + Copilot)
- Disk: 2 GB (Fusion add-in + models)
- Network: Optional (offline mode supported)

### Recommended
- CPU: 8+ cores
- RAM: 16+ GB (better for local LLMs)
- GPU: NVIDIA/AMD for local LLM acceleration
- Disk: 10+ GB (if using large local models)

## Network

### Cloud LLM (OpenAI)
- Requires internet connection
- API key required (https://platform.openai.com)
- Costs per token (~$0.03/1K tokens for GPT-4)

### Local LLM (Ollama)
- No internet required after model download
- Runs on local machine (http://localhost:11434)
- Free, open-source models available

### Offline Mode
- No internet required
- Uses code templates and simple heuristics
- Limited capability, useful for basic features

## Configuration

See `config.py` for all available settings.

Key environment variables:
```bash
OPENAI_API_KEY=sk-...
OLLAMA_API_BASE=http://localhost:11434
FUSION_COPILOT_LOG_LEVEL=INFO
```
