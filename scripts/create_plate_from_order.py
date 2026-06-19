#!/usr/bin/env python3
import bpy, os, sys, argparse
from pathlib import Path

GOON_PLATES_ROOT = Path(__file__).parent.parent
PRESETS = {"moto": {"blank": str(GOON_PLATES_ROOT / "references" / "blanks" / "magnetic smart moto plate blank.stl"),
                    "width_mm": 180.0, "target_text_width_mm": 166.0}}
font = None

def clear_scene():
    for obj in list(bpy.data.objects): bpy.data.objects.remove(obj, do_unlink=True)

def load_font(p):
    try: return bpy.data.fonts.load(p) if os.path.exists(p) else None
    except: return None

def auto_size(text, font_obj, start=80, min_sz=20, max_h_mm=90):
    tw_m = 0.166
    max_h_m = max_h_mm / 1000
    sz = start
    while sz >= min_sz:
        c = bpy.data.curves.new("T", type='FONT')
        c.body, c.size, c.font = text, sz/1000, font_obj
        o = bpy.data.objects.new("T", c)
        bpy.context.scene.collection.objects.link(o)
        if o.dimensions.x <= tw_m and o.dimensions.y <= max_h_m:
            bpy.data.objects.remove(o); bpy.data.curves.remove(c)
            return sz
        bpy.data.objects.remove(o); bpy.data.curves.remove(c)
        sz -= 0.5
    return min_sz

def main():
    global font
    argv = sys.argv
    argv = argv[argv.index('--')+1:] if '--' in argv else []
    p = argparse.ArgumentParser(); p.add_argument("--order-num", default="test")
    p.add_argument("--center-text", default="GOON"); p.add_argument("--preset", default="moto")
    args = p.parse_args(argv)
    
    blank_path = PRESETS[args.preset]["blank"]
    workflow_dir = str(GOON_PLATES_ROOT / "plates")
    font_path = str(GOON_PLATES_ROOT / "references" / "fonts" / "dealerplate" / "dealerplate.california.ttf")
    
    clear_scene(); font = load_font(font_path)
    bpy.ops.wm.stl_import(filepath=blank_path)
    plate = next((o for o in bpy.context.scene.objects if o.type=='MESH'), None)
    if not plate: return
    
    wv = [plate.matrix_world @ v.co for v in plate.data.vertices]
    min_y, max_y, max_z = min(v.y for v in wv), max(v.y for v in wv), max(v.z for v in wv)
    
    # Position text 50mm from TOP edge
    text_h = auto_size(args.center_text, font) / 1000
    y_pos = max_y - 0.050 - text_h/2
    
    print(f"Text height: {text_h*1000:.1f}mm, Y pos: {y_pos:.3f}")
    
    c = bpy.data.curves.new("T", type='FONT')
    c.body, c.size, c.font = args.center_text, text_h, font
    c.align_x, c.align_y = 'CENTER', 'CENTER'
    obj = bpy.data.objects.new("T", c)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = ((min(v.x for v in wv)+max(v.x for v in wv))/2, y_pos, max_z)
    
    bpy.context.view_layer.objects.active = obj; obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    bpy.context.view_layer.objects.active = plate
    m = plate.modifiers.new("E", 'BOOLEAN'); m.operation='DIFFERENCE'; m.object=obj
    bpy.ops.object.modifier_apply(modifier="E")
    bpy.data.objects.remove(obj)
    
    out = Path(workflow_dir) / f"plate_{args.center_text.replace(' ','_')}_{args.order_num}_final.stl"
    bpy.ops.wm.stl_export(filepath=str(out))
    print(f"Final: {out}")

if __name__ == "__main__": main()
