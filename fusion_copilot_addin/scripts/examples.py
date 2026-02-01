"""
Example scripts demonstrating Copilot usage
"""

# Example 1: Parametric Bracket
PARAMETRIC_BRACKET_EXAMPLE = """
# This example shows how the Copilot can generate parametric parts
# User says: "Create a parametric bracket with width/height/thickness parameters"

def create_parametric_bracket(doc, width=100, height=50, thickness=10):
    '''Create a parametric bracket with user parameters'''
    
    design = doc.design
    root = design.rootComponent
    
    # Create user parameters
    params = design.userParameters
    width_param = params.itemByName('BracketWidth') if params.itemByName('BracketWidth') else params.add('BracketWidth', adsk.core.ValueInput.createByReal(width), 'mm')
    height_param = params.itemByName('BracketHeight') if params.itemByName('BracketHeight') else params.add('BracketHeight', adsk.core.ValueInput.createByReal(height), 'mm')
    thick_param = params.itemByName('BracketThickness') if params.itemByName('BracketThickness') else params.add('BracketThickness', adsk.core.ValueInput.createByReal(thickness), 'mm')
    
    # Create sketch
    sketches = root.sketches
    sketch = sketches.add(root.xYConstructionPlane)
    
    # Draw rectangle
    lines = sketch.sketchCurves.sketchLines
    p1 = adsk.core.Point3D.create(0, 0, 0)
    p2 = adsk.core.Point3D.create(width, 0, 0)
    p3 = adsk.core.Point3D.create(width, height, 0)
    p4 = adsk.core.Point3D.create(0, height, 0)
    
    lines.addByTwoPoints(p1, p2)
    lines.addByTwoPoints(p2, p3)
    lines.addByTwoPoints(p3, p4)
    lines.addByTwoPoints(p4, p1)
    
    sketch.close()
    
    # Create extrude
    profile = sketch.profiles.item(0)
    extrudes = root.features.extrudeFeatures
    extrude_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    extrude_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(thickness))
    extrude = extrudes.add(extrude_input)
    extrude.name = 'BracketBase'
    
    return extrude

# The AI generates this code and the user can accept, run, and iterate
"""

# Example 2: CAM Setup
CAM_SETUP_EXAMPLE = """
# User says: "Create a 3-axis setup for face milling"

def create_cam_setup(doc):
    '''Create a CAM setup for face milling'''
    
    cam = doc.cam
    if not cam:
        print("CAM workspace not available")
        return None
    
    # Create setup
    setups = cam.setups
    setup_input = setups.createInput()
    setup_input.name = "Face Mill Setup"
    
    # Configure setup (WCS, tool, etc.)
    # ...
    
    setup = setups.add(setup_input)
    return setup
"""

# Example 3: Drawing Generation
DRAWING_GENERATION_EXAMPLE = """
# User says: "Create a drawing with top, front, and side views"

def create_drawing(doc):
    '''Create a drawing from the design'''
    
    drawings = doc.drawings
    if not drawings:
        print("Drawings not available")
        return None
    
    # Create drawing
    sheet = drawings.add()
    
    # Add views
    # ...
    
    return sheet
"""

EXAMPLES = {
    "parametric_bracket": PARAMETRIC_BRACKET_EXAMPLE,
    "cam_setup": CAM_SETUP_EXAMPLE,
    "drawing_generation": DRAWING_GENERATION_EXAMPLE,
}
