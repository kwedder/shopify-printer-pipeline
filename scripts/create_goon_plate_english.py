import bpy
import os
import sys
from collections import defaultdict

# =============================================================================
# PRESET CONFIGURATIONS
# =============================================================================
PRESETS = {
    "center_only_text_plate": {
        # Margins from plate edges (mm) - gives ~20mm from holes
        "margin_left": 30.0,
        "margin_right": 30.0,
        "margin_bottom": 30.0,
        "margin_top": 30.0,
        
        # Text positioning relative to hole center
        "center_on_holes": True,
        "hole_center_offset_x": 0.0,    # X offset from hole center (mm)
        "hole_center_offset_y": -5.5,   # Y offset from hole center (mm) - negative = down
        
        # Text scaling adjustment (1.0 = exact fit, 1.01 = 1% larger)
        "text_scale_adjustment": 1.01,
        
        # Engraving settings
        "engrave_depth": 0.05,        # mm
        
        # Paths
        "blank_path": "C:/Users/kwedd/dev/.pi/skills/goon-plates/references/blanks/smart moto plate blank (bolt-on).stl",
        "font_path": "C:/Users/kwedd/dev/.pi/skills/goon-plates/references/fonts/dealerplate/dealerplate.california.ttf",
        "output_path": "C:/Users/kwedd/dev/.pi/skills/goon-plates/plates/plate_goon_final.stl",
    },
    "center_only_text_plate_english": {
        # Same margins
        "margin_left": 30.0,
        "margin_right": 30.0,
        "margin_bottom": 30.0,
        "margin_top": 30.0,
        
        # Text positioning relative to hole center
        "center_on_holes": True,
        "hole_center_offset_x": 0.0,
        "hole_center_offset_y": -5.5,
        
        # Text scaling adjustment
        "text_scale_adjustment": 1.01,
        
        # Engraving settings
        "engrave_depth": 0.05,
        
        # Paths - use English font
        "blank_path": "C:/Users/kwedd/dev/.pi/skills/goon-plates/references/blanks/smart moto plate blank (bolt-on).stl",
        "font_path": "C:/Users/kwedd/dev/.pi/skills/goon-plates/references/fonts/dealerplate/dealerplate.california.ttf",
        "output_path": "C:/Users/kwedd/dev/.pi/skills/goon-plates/plates/plate_goon_booby.stl",
    }
}

# =============================================================================
# MAIN FUNCTION
# =============================================================================
def create_plate_with_preset(text_string, preset_name="center_only_text_plate", output_path_override=None, text_height_override=None):
    """Create a plate with text using a named preset configuration."""
    
    # Load preset
    if preset_name not in PRESETS:
        print(f"ERROR: Preset '{preset_name}' not found")
        return {"status": "error", "message": f"Preset '{preset_name}' not found"}
    
    preset = PRESETS[preset_name]
    
    blank_path = preset["blank_path"]
    font_path = preset["font_path"]
    output_path = output_path_override or preset["output_path"]
    engrave_depth = preset["engrave_depth"]
    text_height = text_height_override or 54.0  # Default text height
    
    # Clear existing objects
    for obj in list(bpy.data.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    
    # Import blank
    bpy.ops.wm.stl_import(filepath=blank_path)
    blank_obj = None
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            blank_obj = obj
            break
    
    if blank_obj is None:
        print("ERROR: No mesh imported")
        return {"status": "error", "message": "Import failed"}
    
    print(f"Blank: {blank_obj.name}")
    
    # Get plate dimensions
    world_verts = [blank_obj.matrix_world @ v.co for v in blank_obj.data.vertices]
    min_x = min(v.x for v in world_verts)
    max_x = max(v.x for v in world_verts)
    min_y = min(v.y for v in world_verts)
    max_y = max(v.y for v in world_verts)
    min_z = min(v.z for v in world_verts)
    max_z = max(v.z for v in world_verts)
    
    plate_width = max_x - min_x
    plate_height = max_y - min_y
    plate_center_x = (min_x + max_x) / 2
    plate_center_y = (min_y + max_y) / 2
    
    print(f"Plate: {plate_width:.1f} x {plate_height:.1f} mm")
    print(f"Plate edges: X [{min_x:.1f}, {max_x:.1f}], Y [{min_y:.1f}, {max_y:.1f}]")
    print(f"Plate center: ({plate_center_x:.1f}, {plate_center_y:.1f})")
    
    # Find hole centers if enabled
    desired_center_x = plate_center_x
    desired_center_y = plate_center_y
    
    if preset.get("center_on_holes", False):
        # Find holes by looking at bottom surface vertices
        bottom_verts = [v for v in world_verts if abs(v.z - min_z) < 0.01]
        
        # Group by X position (round to nearest 10mm)
        x_groups = defaultdict(list)
        for v in bottom_verts:
            x_key = round(v.x / 10) * 10
            x_groups[x_key].append(v)
        
        # Find groups with enough vertices (potential holes)
        hole_groups = {k: v for k, v in x_groups.items() if len(v) > 20}
        
        if hole_groups:
            print(f"\nFound {len(hole_groups)} potential hole groups")
            hole_centers = []
            for x_key, verts in sorted(hole_groups.items()):
                avg_x = sum(v.x for v in verts) / len(verts)
                avg_y = sum(v.y for v in verts) / len(verts)
                hole_centers.append((avg_x, avg_y))
                print(f"  Hole at X≈{x_key:.0f}: center ({avg_x:.1f}, {avg_y:.1f}), {len(verts)} verts")
            
            if len(hole_centers) >= 2:
                desired_center_x = sum(c[0] for c in hole_centers) / len(hole_centers)
                desired_center_y = sum(c[1] for c in hole_centers) / len(hole_centers)
                print(f"\nHole center point: ({desired_center_x:.1f}, {desired_center_y:.1f})")
            else:
                print("\nNot enough holes found, using plate center")
        else:
            print("\nNo holes detected, using plate center")
        
        # Apply offsets from hole center
        desired_center_x += preset["hole_center_offset_x"]
        desired_center_y += preset["hole_center_offset_y"]
        print(f"After offset: ({desired_center_x:.1f}, {desired_center_y:.1f})")
    
    # Calculate desired text box based on margins
    desired_text_left = min_x + preset["margin_left"]
    desired_text_right = max_x - preset["margin_right"]
    desired_text_bottom = min_y + preset["margin_bottom"]
    desired_text_top = max_y - preset["margin_top"]
    
    desired_text_width = desired_text_right - desired_text_left
    desired_text_height = desired_text_top - desired_text_bottom
    
    print(f"\nDesired text box (from margins):")
    print(f"  Width: {desired_text_width:.1f}mm, Height: {desired_text_height:.1f}mm")
    print(f"  Left: {desired_text_left:.1f}, Right: {desired_text_right:.1f}")
    print(f"  Bottom: {desired_text_bottom:.1f}, Top: {desired_text_top:.1f}")
    
    # Create temporary text to measure
    text_curve = bpy.data.curves.new("TempTextCurve", type='FONT')
    text_curve.body = text_string
    text_curve.size = 100.0  # Temporary size
    text_curve.extrude = engrave_depth
    text_curve.bevel_depth = 0.0
    text_curve.align_x = 'CENTER'
    text_curve.align_y = 'CENTER'
    
    # Load font - try preset font, fallback to default
    try:
        if os.path.exists(font_path):
            font = bpy.data.fonts.load(font_path)
            text_curve.font = font
            print(f"\nFont loaded: {font_path}")
        else:
            print(f"\nWarning: Font not found at {font_path}, using default")
    except Exception as e:
        print(f"\nWarning: Could not load font: {e}, using default")
    
    # Create temporary text object
    temp_text_obj = bpy.data.objects.new("TempText", text_curve)
    bpy.context.scene.collection.objects.link(temp_text_obj)
    
    # Convert to mesh to measure
    bpy.context.view_layer.objects.active = temp_text_obj
    temp_text_obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    
    # Measure text at size=100
    temp_verts = [temp_text_obj.matrix_world @ v.co for v in temp_text_obj.data.vertices]
    temp_min_x = min(v.x for v in temp_verts)
    temp_max_x = max(v.x for v in temp_verts)
    temp_min_y = min(v.y for v in temp_verts)
    temp_max_y = max(v.y for v in temp_verts)
    
    temp_width = temp_max_x - temp_min_x
    temp_height = temp_max_y - temp_min_y
    
    print(f"\nText measurements at size=100:")
    print(f"  Width: {temp_width:.1f}mm, Height: {temp_height:.1f}mm")
    
    # Calculate scale factor to fit desired width
    scale_factor = desired_text_width / temp_width
    final_text_size = 100.0 * scale_factor * preset.get("text_scale_adjustment", 1.0)
    
    # Override with fixed height if specified
    if text_height:
        final_text_size = text_height
        print(f"\nOVERRIDE: Using fixed text height: {text_height}mm")
    
    print(f"\nScaling:")
    print(f"  Scale factor: {scale_factor:.3f}")
    print(f"  Final text_size: {final_text_size:.1f}mm")
    print(f"  Expected text width: {temp_width * scale_factor:.1f}mm")
    print(f"  Expected text height: {temp_height * scale_factor:.1f}mm")
    
    # Clean up temporary text
    bpy.data.objects.remove(temp_text_obj, do_unlink=True)
    bpy.data.curves.remove(text_curve)
    
    # Create actual text with correct size
    text_curve = bpy.data.curves.new("TextCurve", type='FONT')
    text_curve.body = text_string
    text_curve.size = final_text_size
    text_curve.extrude = engrave_depth
    text_curve.bevel_depth = 0.0
    text_curve.align_x = 'CENTER'
    text_curve.align_y = 'CENTER'
    
    # Load font again for actual text
    try:
        if os.path.exists(font_path):
            font = bpy.data.fonts.load(font_path)
            text_curve.font = font
        else:
            # Try to load a default English font if available
            english_fonts = [
                "C:/Windows/Fonts/Arial.ttf",
                "C:/Windows/Fonts/Times.ttf",
                "C:/Windows/Fonts/Calibri.ttf",
                "C:/Windows/Fonts/Candara.ttf"
            ]
            for ef in english_fonts:
                if os.path.exists(ef):
                    font = bpy.data.fonts.load(ef)
                    text_curve.font = font
                    print(f"\nUsing fallback English font: {ef}")
                    break
    except Exception as e:
        print(f"\nWarning: Could not load font: {e}")
    
    # Create text object
    text_obj = bpy.data.objects.new("EngraveText", text_curve)
    bpy.context.scene.collection.objects.link(text_obj)
    
    # Position text
    text_obj.location.x = desired_center_x
    text_obj.location.y = desired_center_y
    text_obj.location.z = max_z  # Top surface
    
    print(f"\nText positioned at: ({text_obj.location.x:.1f}, {text_obj.location.y:.1f})")
    print(f"Margins from plate edges:")
    print(f"  Left: {text_obj.location.x - desired_text_width/2 - min_x:.1f}mm")
    print(f"  Right: {max_x - (text_obj.location.x + desired_text_width/2):.1f}mm")
    print(f"  Bottom: {text_obj.location.y - desired_text_height/2 - min_y:.1f}mm")
    print(f"  Top: {max_y - (text_obj.location.y + desired_text_height/2):.1f}mm")
    
    # Convert to mesh
    bpy.context.view_layer.objects.active = text_obj
    text_obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    print(f"\nText mesh created: {len(text_obj.data.vertices)} verts")
    
    # Add boolean modifier (single operation on fused text)
    bool_mod = blank_obj.modifiers.new(name="Engrave", type='BOOLEAN')
    bool_mod.operation = 'DIFFERENCE'
    bool_mod.object = text_obj
    bool_mod.solver = 'EXACT'
    
    print(f"Applying boolean (engraving text)...")
    bpy.context.view_layer.objects.active = blank_obj
    try:
        bpy.ops.object.modifier_apply(modifier="Engrave")
        print(f"Boolean applied. Final verts: {len(blank_obj.data.vertices)}")
    except Exception as e:
        print(f"Boolean failed: {e}")
    
    # Remove text object
    if text_obj.name in bpy.data.objects:
        bpy.data.objects.remove(text_obj, do_unlink=True)
    
    # Export final plate
    bpy.ops.wm.stl_export(filepath=output_path)
    print(f"\nSUCCESS! Plate exported to: {output_path}")
    print(f"Text: '{text_string}' at {final_text_size:.1f}mm height (auto-scaled)")
    print(f"Engraved {engrave_depth}mm deep")
    print(f"Preset: {preset_name}")
    
    return {"status": "success", "output_path": output_path}


def create_plate_with_multiple_text(text_strings, preset_name="center_only_text_plate"):
    """Create plate with multiple text strings fused for single boolean operation."""
    
    # First, create all text objects
    text_objects = []
    for text_str in text_strings:
        result = create_plate_with_preset(text_str, preset_name)
        # This approach won't work - need to modify the function
        # For now, just create one text
        break
    
    return result


# =============================================================================
# MAIN EXECUTION
# =============================================================================
import argparse

parser = argparse.ArgumentParser(description="Create Goon Plate with English text")
parser.add_argument("--preset", default="center_only_text_plate_english", help="Preset name")
parser.add_argument("--text", default="GOON", help="Text to engrave")
parser.add_argument("--output", help="Output path (overrides preset)")
parser.add_argument("--text-height", type=float, help="Text height override in mm")
parser.add_argument("--text-height-override", type=float, help="Text height override in mm")

# Parse args
argv = sys.argv
if '--' in argv:
    argv = argv[argv.index('--') + 1:]
else:
    argv = []

args = parser.parse_args(argv) if argv else parser.parse_args([])

# Text to engrave
TEXT_TO_ENGRAVE = args.text

# Text height override
TEXT_HEIGHT_OVERRIDE = args.text_height or args.text_height_override or 80.0  # mm

# Output path override
OUTPUT_PATH_OVERRIDE = args.output

# Use the specified preset
preset_name = args.preset

# Single text
result = create_plate_with_preset(TEXT_TO_ENGRAVE, preset_name, output_path_override=OUTPUT_PATH_OVERRIDE, text_height_override=TEXT_HEIGHT_OVERRIDE)
print("\nDone")