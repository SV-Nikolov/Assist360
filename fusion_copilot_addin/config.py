"""
Configuration for Fusion 360 Copilot Assistant
"""

# Model Configuration
MODEL_CONFIG = {
    "default_backend": "openai",  # Options: "openai", "local", "offline"
    "openai": {
        "model": "gpt-4",
        "api_endpoint": "https://api.openai.com/v1",
        "temperature": 0.7,
        "max_tokens": 2048,
    },
    "local": {
        "model": "neural-chat",  # Ollama model name
        "api_endpoint": "http://localhost:11434",
        "temperature": 0.7,
        "max_tokens": 2048,
    },
    "offline": {
        "mode": "templates",
        "template_dir": "scripts/templates/",
    }
}

# Prompt Configuration
PROMPT_CONFIG = {
    "system_prompt_type": "fusion_expert",
    "max_context_size": 8000,  # Tokens
    "include_parameter_defaults": True,
    "include_recent_features": True,
    "max_recent_features": 5,
}

# Execution Configuration
EXECUTION_CONFIG = {
    "timeout_seconds": 60,
    "auto_transaction": True,
    "capture_output": True,
    "max_retries_on_error": 2,
    "sandbox_mode": True,
}

# UI Configuration
UI_CONFIG = {
    "theme": "auto",  # Options: "light", "dark", "auto"
    "panel_width": "400px",
    "max_visible_lines": 250,
    "syntax_highlight": True,
    "show_context_panel": True,
}

# Project Integration
PROJECT_CONFIG = {
    "scan_on_startup": True,
    "max_file_size_mb": 100,
    "supported_geometry": ["stl", "step", "stp", "iges", "igs", "obj"],
    "supported_docs": ["txt", "md", "json", "pdf"],
    "supported_images": ["png", "jpg", "jpeg", "bmp"],
}

# Feature Flags
FEATURES = {
    "enable_inline_completions": False,  # Phase 3
    "enable_cam_generation": False,      # Phase 3
    "enable_drawing_generation": False,  # Phase 3
    "enable_geometry_analysis": False,   # Phase 3
    "enable_vision_import": False,       # Phase 3
}

# Logging
LOGGING_CONFIG = {
    "level": "INFO",
    "file": "fusion_copilot.log",
    "max_size_mb": 10,
}

def get_config(key, default=None):
    """Get configuration value"""
    parts = key.split(".")
    config = globals().get(f"{parts[0]}_CONFIG", {})
    
    for part in parts[1:]:
        if isinstance(config, dict):
            config = config.get(part)
        else:
            return default
    
    return config if config is not None else default
