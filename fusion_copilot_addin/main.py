"""
Fusion 360 Copilot-Style Assistant
Main entry point for the Fusion 360 add-in
"""

import adsk.core
import adsk.fusion
import adsk.cam
import traceback
import json
import os
from pathlib import Path

from core.orchestrator import Orchestrator
from core.context import ContextCapture
from core.executor import CodeExecutor

# Global variables
app = None
ui = None
handlers = []
orchestrator = None
context_capture = None
executor = None


def run(context):
    """Main entry point for the add-in"""
    try:
        global app, ui, handlers, orchestrator, context_capture, executor
        
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Initialize core components
        context_capture = ContextCapture(app)
        executor = CodeExecutor(app)
        orchestrator = Orchestrator(app, context_capture, executor)
        
        # Create UI palette
        _create_palette(ui, orchestrator)
        
        # Register commands
        _register_commands(ui, orchestrator)
        
        ui.messageBox("Fusion 360 Copilot Assistant loaded successfully!")
        
    except Exception as e:
        ui.messageBox(f"Error loading Copilot Assistant: {str(e)}\n{traceback.format_exc()}")


def _create_palette(ui, orchestrator):
    """Create the docked chat palette"""
    try:
        # Get the palette resources path
        addin_path = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(addin_path, "ui", "panel.html")
        
        # Create palette
        palette = ui.palettes.add(
            id="fusion_copilot_palette",
            name="Copilot Assistant",
            htmlPath=html_path,
            isVisible=True
        )
        
        # Store orchestrator reference for palette communication
        palette.orchestrator = orchestrator
        
    except Exception as e:
        ui.messageBox(f"Error creating palette: {str(e)}")


def _register_commands(ui, orchestrator):
    """Register command buttons and hotkeys"""
    try:
        # Create command definitions
        # These will be used for toolbar buttons and context menus
        pass
        
    except Exception as e:
        ui.messageBox(f"Error registering commands: {str(e)}")


def stop(context):
    """Clean up when add-in is stopped"""
    try:
        global handlers
        for handler in handlers:
            handler.disconnect()
    except Exception as e:
        if ui:
            ui.messageBox(f"Error stopping add-in: {str(e)}")
