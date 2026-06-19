import bpy
import os
from collections import defaultdict

# =============================================================================
# FULL PLATE CREATION WORKFLOW
# =============================================================================
# This script:
# 1. Takes a blank plate
# 2. Adds GOON (70mm height) and exports
# 3. Imports, adds TEST (20mm at Y=159.7) and exports
# 4. Imports, adds BELOW (20mm at Y=89.7) and exports final

# =============================================================================
# CONFIGURATION
# =============================================================================
import sys
import os as os_module

# Shopify Order Integration
# Set these values from Shopify order custom attributes:
# - center_text -> GOON_TEXT (main text)
# - top_text -> TEST_TEXT 
# - bottom_text -> BELOW_TEXT
# If no order data provided, use defaults
def get_order_data():
    """Get order data from command line args or environment."""
    center_text = "GOON"
    top_text = "TEST"
    bottom_text = "BELOW"
    
    # Check command line args first
    args = sys.argv
    if "--center-text" in args:
        idx = args.index("--center-text")
        if idx + 1 < len(args):
            center_text = args[idx + 1]
    if "--top-text" in args:
        idx = args.index("--top-text")
        if idx + 1 < len(args):
            top_text = args[idx + 1]
    if "--bottom-text" in args:
        idx = args.index("--bottom-text")
        if idx + 1 < len(args):
            bottom_text = args[idx + 1]
    
    return center_text, top_text, bottom_text

# Get text values from Shopify order (or use defaults)
GOON_TEXT, TEST_TEXT, BELOW_TEXT = get_order_data()

BLANK_PATH = "C:/Users/kwedd/dev/.pi/skills/goon-plates/references/blanks/moto plate blank (bolt on).stl"
FONT_PATH = "C:/Users/kwedd/dev/.pi/skills/goon-plates/references/fonts/dealerplate.california.ttf"
WORKFLOW_DIR = "C:/Users/kwedd/dev/.pi/skills/goon-plates/plates"

# Text settings
GOON_TEXT_HEIGHT = 70.0
GOON_ENGRAVE_DEPTH = 0.05
GOON_Y_OFFSET = -5.5

TEST_TEXT_HEIGHT = 20.0
TEST_ENGRAVE_DEPTH = 0.05
TEST_Y_POS = 159.7

BELOW_TEXT_HEIGHT = 20.0
BELOW_ENGRAVE_DEPTH = 0.05
BELOW_Y_POS = 89.7

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def clear_scene():
    """Clear all objects from the scene."""
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)

def load_font(font_path):
    """Load font, fallback to default if not found."""
    try:
        if os.path.exists(font_path):
            return bpy.data.fonts.load(font_path)
    except Exception as e:
        print(f"Warning: Could not load font: {e}")
    return None

def create_text_object(text_string, text_size, extrude, font, position):
    """Create a text object with extrusion for engraving."""
    text_curve = bpy.data.curves.new("EngraveText", type='FONT')
    text_curve.body = text_string
    text_curve.size = text_size
    text_curve.extrude = extrude  # KEY: Extrude BEFORE mesh conversion
    text_curve.bevel_depth = 0.0
    text_curve.align_x = 'CENTER'
    text_curve.align_y = 'CENTER'
    
    if font:
        text_curve.font = font
    
    text_obj = bpy.data.objects.new("EngraveText", text_curve)
    bpy.context.scene.collection.objects.link(text_obj)
    text_obj.location = position
    
    return text_obj

def apply_boolean(plate_obj, text_obj):
    """Apply boolean difference to engrave text into plate."""
    bool_mod = plate_obj.modifiers.new(name="Engrave", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = text_obj
    bool_mod.solver = 'EXACT'
    
    bpy.context.view_layer.objects.active = plate_obj
    bpy.ops.object.modifier_apply(modifier="Engrave")

def get_plate_center(plate_obj):
    """Get plate center Y."""
    world_verts = [plate_obj.matrix_world @ v.co for v in plate_obj.data.vertices]
    min_y = min(v.y for v in world_verts)
    max_y = max(v.y for v in world_verts)
    return (min_y + max_y) / 2

def process_step(plate_obj, text_string, text_height, y_pos, step_name, export_path):
    """Process one text addition step."""
    # Skip if text is empty
    if not text_string or not text_string.strip():
        print(f"\n--- STEP: {step_name} (SKIPPED - empty text) ---")
        return plate_obj
    
    print(f"\n--- STEP: {step_name} ---")
    
    # Create text
    text_obj = create_text_object(
        text_string=text_string,
        text_size=text_height,
        extrude=0.05,
        font=font,
        position=(dims['center_x'], y_pos, dims['max_z'])
    )
    
    # Convert to mesh
    bpy.context.view_layer.objects.active = text_obj
    text_obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    print(f"{text_string} mesh created: {len(text_obj.data.vertices)} verts")
    
    # Apply boolean
    apply_boolean(plate_obj, text_obj)
    print(f"{text_string} engraved. Plate verts: {len(plate_obj.data.vertices)}")
    
    # Remove text object
    bpy.data.objects.remove(text_obj, do_unlink=True)
    
    # Export
    bpy.ops.wm.stl_export(filepath=export_path)
    print(f"Exported to: {export_path}")
    
    return plate_obj

# =============================================================================
# MAIN
# =============================================================================
print("=== FULL PLATE CREATION WORKFLOW ===")

# Clear scene
clear_scene()

# Load font
font = load_font(FONT_PATH)
if font:
    print(f"Font loaded: {FONT_PATH}")

# Import blank
bpy.ops.wm.stl_import(filepath=BLANK_PATH)
plate_obj = None
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        plate_obj = obj
        break

if plate_obj is None:
    print("ERROR: No mesh imported")
    exit(1)

print(f"Blank: {plate_obj.name}")

# Get dimensions
world_verts = [plate_obj.matrix_world @ v.co for v in plate_obj.data.vertices]
min_x = min(v.x for v in world_verts)
max_x = max(v.x for v in world_verts)
min_y = min(v.y for v in world_verts)
max_y = max(v.y for v in world_verts)
min_z = min(v.z for v in world_verts)
max_z = max(v.z for v in world_verts)
dims = {
    'center_x': (min_x + max_x) / 2,
    'center_y': (min_y + max_y) / 2,
    'max_z': max_z
}
print(f"Plate dimensions: {max_x - min_x:.1f} x {max_y - min_y:.1f} mm")

# =============================================================================
# STEP 1: Add GOON
# =============================================================================
goon_path = os.path.join(WORKFLOW_DIR, "temp_goon.stl")
process_step(plate_obj, GOON_TEXT, GOON_TEXT_HEIGHT, dims['center_y'] + GOON_Y_OFFSET, "GOON", goon_path)

# =============================================================================
# STEP 2: Import and Add TEST
# =============================================================================
clear_scene()
bpy.ops.wm.stl_import(filepath=goon_path)
plate_obj = None
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        plate_obj = obj
        break

process_step(plate_obj, TEST_TEXT, TEST_TEXT_HEIGHT, TEST_Y_POS, "TEST", os.path.join(WORKFLOW_DIR, "temp_test.stl"))

# =============================================================================
# STEP 3: Import and Add BELOW
# =============================================================================
clear_scene()
bpy.ops.wm.stl_import(filepath=os.path.join(WORKFLOW_DIR, "temp_test.stl"))
plate_obj = None
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        plate_obj = obj
        break

process_step(plate_obj, BELOW_TEXT, BELOW_TEXT_HEIGHT, BELOW_Y_POS, "BELOW", os.path.join(WORKFLOW_DIR, "plate_goon_test_final.stl"))

# =============================================================================
# CLEANUP
# =============================================================================
import os as os_module
for f in ["temp_goon.stl", "temp_test.stl"]:
    try:
        os_module.remove(os.path.join(WORKFLOW_DIR, f))
    except:
        pass

print("\n=== WORKFLOW COMPLETE ===")
print(f"Final plate: plate_goon_test_final.stl")
print(f"GOON: {GOON_TEXT} ({GOON_TEXT_HEIGHT}mm at Y offset {GOON_Y_OFFSET})")
print(f"TEST: {TEST_TEXT} ({TEST_TEXT_HEIGHT}mm at Y={TEST_Y_POS})")
print(f"BELOW: {BELOW_TEXT} ({BELOW_TEXT_HEIGHT}mm at Y={BELOW_Y_POS}")